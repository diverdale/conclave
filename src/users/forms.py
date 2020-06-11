from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.widgets.html5 import EmailInput
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo
from wtforms import ValidationError
from src.models import User, Role


class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()], widget=EmailInput())
    user_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    user_email = StringField('Email', [DataRequired(), Email()], widget=EmailInput())
    user_username = StringField('Username', validators=[DataRequired()])
    user_password = PasswordField('Password', validators=[DataRequired(),
                                                          EqualTo('pass_confirm', message='Passwords mismatch')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        print(field)
        if User.query.filter_by(user_email=field).first():
            return True

    def check_username(self, field):
        if User.query.filter_by(user_username=field).first():
            return True


class EditUserForm(FlaskForm):
    choices = Role.query.all()
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_username = StringField('Username', validators=[DataRequired()])
    user_role = SelectField('Role', choices=[(choice.role_name, choice.role_name)
                                             for choice in choices], default=2)
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password:', validators=[DataRequired(),
                                                              EqualTo('password_confirm', message='Passwords mismatch')])
    password_confirm = PasswordField('Confirm Password:', validators=[DataRequired()])

    submit = SubmitField('Submit')


class UserProfileForm(FlaskForm):
    choices = Role.query.all()
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_username = StringField('Username', validators=[DataRequired()])
    user_role = SelectField('Role', choices=[(choice.role_name, choice.role_name)
                                             for choice in choices], default=2)
    user_first_name = StringField('First Name')
    user_last_name = StringField('Last Name')
    # user_birthday = DateField('Birthday')
    user_location = StringField('Location')
    user_about = StringField('About Me')
    user_occupation = StringField('Occupation')
    user_interests = StringField('Interests')

    submit = SubmitField('Submit')
