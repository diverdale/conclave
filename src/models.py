from src import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(64), unique=True, index=True)
    user_username = db.Column(db.String(64), unique=True, index=True)
    user_posts = db.relationship('Topic', cascade="all, delete-orphan", backref='author', lazy='dynamic')
    user_role = db.Column(db.String(10), index=True, default='User')
    user_first_name = db.Column(db.String(64), index=True, nullable=True)
    user_last_name = db.Column(db.String(64), index=True, nullable=True)
    user_birthday = db.Column(db.DateTime(), index=True, nullable=True)
    user_date = db.Column(db.DateTime(), index=True, nullable=True)
    user_location = db.Column(db.String(64), index=True, nullable=True)
    user_about = db.Column(db.String(140), index=True, nullable=True)
    user_occupation = db.Column(db.String(100), index=True, nullable=True)
    user_interests = db.Column(db.String(100), index=True, nullable=True)
    password_hash = db.Column(db.String(128))
    user_reply = db.relationship('Reply', cascade="all, delete-orphan", backref='reply_from', lazy='dynamic')

    def __init__(self, user_email, user_username, user_password, user_role,
                 user_date):

        self.user_email = user_email
        self.user_username = user_username
        self.user_role = user_role
        self.password_hash = generate_password_hash(user_password)
        self.user_date = user_date

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    topic_author = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic_title = db.Column(db.String(100))
    topic_date = db.Column(db.DateTime)
    topic_content = db.Column(db.Text)
    topic_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    topic_reply = db.relationship('Reply', cascade="all, delete-orphan", backref='reply', lazy='dynamic')

    def __init__(self, topic_title, topic_content, topic_author, topic_date, topic_category):
        self.topic_title = topic_title
        self.topic_content = topic_content
        self.topic_author = topic_author
        self.topic_date = topic_date
        self.topic_category = topic_category

    def __repr__(self):
        return self.topic_title


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100))
    category_description = db.Column(db.String(100))
    category_topic = db.relationship('Topic', cascade="all, delete-orphan", backref='top_author', lazy='dynamic')

    def __init__(self, category_name, category_description):
        self.category_name = category_name
        self.category_description = category_description

    def __repr__(self):
        return self.category_name


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    reply_content = db.Column(db.Text)
    reply_date = db.Column(db.DateTime)
    reply_topic = db.Column(db.Integer, db.ForeignKey('topic.id'))
    reply_author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, reply_content, reply_date, reply_topic, reply_author):
        self.reply_content = reply_content
        self.reply_date = reply_date
        self.reply_topic = reply_topic
        self.reply_author = reply_author

    def __repr__(self):
        return f'reply'


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(25))

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return self._title
