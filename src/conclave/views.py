from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import current_user, login_required
from src import app, db
from src.models import Topic, Category, User, Reply
from src.conclave.forms import NewTopicForm, ReplyTopicForm, EditTopicForm, AddCategoryForm
import datetime
from sqlalchemy.sql.functions import func

conclave = Blueprint('conclave', __name__,
                     template_folder='templates/forum')


@conclave.route('/')
def index():
    # topics = Topic.query.all()
    categories = Category.query.all()
    # replies = db.session.query(Topic, func.count(Reply.reply_topic)).outerjoin(Topic, Reply.reply_topic == Topic.id)\
    #     .group_by(Topic.topic_title).all()
    topics = db.session.query(Topic.id, Topic.topic_title, Topic.topic_category, func.count(Reply.reply_topic)
                              .label('count_1')).outerjoin(Topic, Reply.reply_topic == Topic.id).group_by(Topic.topic_title).all()

    return render_template('main.html', topics=topics, categories=categories)


@conclave.route('/category/<int:category_id>')
def category_view(category_id):
    category = Category.query.filter_by(id=category_id).first()
    topics = Topic.query.filter_by(topic_category=category_id).all()
    replies = db.session.query(Topic, func.count(Reply.reply_topic)).outerjoin(Topic, Reply.reply_topic == Topic.id) \
        .group_by(Topic.topic_title).all()
    print(replies)
    return render_template('category_view.html', topics=topics, category=category, replies=replies)


@conclave.route('/<topic_id>')
def view(topic_id):
    replies = Reply.query.filter_by(reply_topic=topic_id).all()
    topic = Topic.query.filter_by(id=topic_id).first()
    original_author = User.query.filter_by(id=topic.topic_author).first()
    # reply_author = User.query.filter_by(id=replies.reply_author)
    print(f'reply author {replies}')
    return render_template('topic_details.html', topic=topic, replies=replies,
                           op=original_author)


@conclave.route('/add', methods=['GET', 'POST'])
def add():
    form = NewTopicForm(request.form)

    if request.method == 'POST' and form.validate():
        new_topic = Topic(topic_title=form.topic_title.data,
                          topic_content=form.topic_content.data,
                          topic_category=form.topic_category.data,
                          topic_date=datetime.datetime.now(),
                          topic_author=current_user.id)
        db.session.add(new_topic)
        db.session.commit()

        return redirect(url_for('conclave.index'))
    return render_template('new_topic.html', form=form)


@conclave.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm(request.form)

    if request.method == 'POST' and form.validate():
        new_category = Category(category_name=form.category_name.data,
                                category_description=form.category_description.data)

        db.session.add(new_category)
        db.session.commit()

        flash('Category Added')
        return redirect(url_for('conclave.index'))
    return render_template('category_add.html', form=form)


@conclave.route('<int:topic_id>/reply', methods=['GET', 'POST'])
def reply(topic_id):
    form = ReplyTopicForm(request.form)
    topic = Topic.query.filter_by(id=topic_id).first()

    if request.method == 'POST' and form.validate():
        new_reply = Reply(reply_content=form.reply_content.data,
                          reply_date=datetime.datetime.now(),
                          reply_topic=topic_id,
                          reply_author=current_user.id)
        db.session.add(new_reply)
        db.session.commit()

        return redirect(url_for('conclave.view', topic_id=topic_id))

    return render_template('topic_reply.html', topic=topic, form=form)


@conclave.route('<int:topic_id>/edit', methods=['GET', 'POST'])
def edit(topic_id):
    topic = Topic.query.get_or_404(topic_id)

    form = EditTopicForm()

    if form.validate_on_submit():
        topic.topic_title = form.topic_title.data
        topic.topic_content = form.topic_content.data

        db.session.commit()
        flash('Topic Updated')
        return redirect(url_for('conclave.view', topic_id=topic_id))

    elif request.method == 'GET':
        form.topic_title.data = topic.topic_title
        form.topic_content.data = topic.topic_content

    return render_template('topic_edit.html', form=form)


@conclave.route('<int:topic_id>/<int:reply_id>/reply_edit', methods=['GET', 'POST'])
def reply_edit(reply_id, topic_id):
    topic_reply = Reply.query.get_or_404(reply_id)
    print(topic_reply.reply_content)

    form = ReplyTopicForm()

    if form.validate_on_submit():
        topic_reply.reply_content = form.reply_content.data
        topic_reply.reply_date = datetime.datetime.now()

        db.session.commit()
        flash('Reply Updated')
        return redirect(url_for('conclave.view', topic_id=topic_id))

    elif request.method == 'GET':
        form.reply_content.data = topic_reply.reply_content

    return render_template('topic_reply_edit.html', form=form)


@conclave.route('/<int:topic_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    flash('Topic Deleted')
    return redirect(url_for('conclave.index'))
