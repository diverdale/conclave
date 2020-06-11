from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo
from wtforms import ValidationError
from src.models import User, Category, Reply


class NewTopicForm(FlaskForm):
    choices = Category.query.all()
    topic_title = StringField('Title', validators=[DataRequired()])
    topic_category = SelectField('Category', coerce=int, choices=[(choice.id, choice.category_name)
                                                                  for choice in choices], default=1)
    topic_content = TextAreaField('Content', render_kw={'rows': 10}, validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddCategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    category_description = StringField('Category Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReplyTopicForm(FlaskForm):
    reply_content = TextAreaField('Message:', render_kw={'rows': 5}, validators=[DataRequired()])
    submit = SubmitField('Reply')


class EditTopicForm(FlaskForm):
    topic_title = StringField('Title', validators=[DataRequired()])
    topic_content = TextAreaField('Content', render_kw={'rows': 10}, validators=[DataRequired()])
    submit = SubmitField('Update')

