from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_user, login_required, logout_user, current_user
from src import app, db
from src.models import User
from src.users.forms import LoginForm, RegistrationForm, EditUserForm
import datetime

users_blueprint = Blueprint('users', __name__,
                            template_folder='templates/users')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()

        if user.check_password(form.user_password.data) and user is not None:

            login_user(user)

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('index')

            return redirect(next)
    return render_template('login.html', form=form)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(user_email=form.user_email.data,
                    user_username=form.user_username.data,
                    user_password=form.user_password.data,
                    user_role='User',
                    user_date=datetime.datetime.now())
        if form.check_email(form.user_email.data):
            flash('Email already exists')

        elif form.check_username(form.user_username.data):
            flash('username exists')

        else:
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering!')

            return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('profile_edit.html', user=user)


@users_blueprint.route('/list')
@login_required
def list():
    users = User.query.all()
    return render_template('list_users.html', users=users)


@users_blueprint.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):

    user = User.query.get_or_404(user_id)
    if current_user.user_role != 'Admin':
        abort(403)
    form = EditUserForm()

    if form.validate_on_submit():
        user.user_username = form.user_username.data
        user.user_email = form.user_email.data
        user.user_role = form.user_role.data
        user.user_password = form.user_password.data
        print(form.submit.label)
        db.session.commit()
        flash('User Updated')
        return redirect(url_for('users.list'))

    elif request.method == 'GET':
        form.user_username.data = user.user_username
        form.user_email.data = user.user_email
        form.user_role.data = user.user_role

    return render_template('edit_user.html', form=form, user_id=user_id)


@users_blueprint.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(user_id):

    user = User.query.get_or_404(user_id)
    if current_user.user_role != 'Admin':
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted')
    return redirect(url_for('users.list'))


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

