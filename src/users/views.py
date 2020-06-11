from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_user, login_required, logout_user, current_user
from src import app, db
from src.models import User
from src.users.forms import (LoginForm, RegistrationForm, EditUserForm,
                             UserProfileForm, ChangePasswordForm)
import datetime

users = Blueprint('users', __name__,
                  template_folder='templates/users')


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user is None or not user.check_password(form.user_password.data):
            flash('Invalid username or password')
            return redirect(url_for('users.login'))
        login_user(user)

        next = request.args.get('next')

        if next == None or not next[0] == '/':
            next = url_for('core.index')

        return redirect(next)
    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
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


@users.route('/list')
@login_required
def list():
    users = User.query.all()
    return render_template('list_users.html', users=users)


@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
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
        db.session.commit()
        flash('User Updated')
        return redirect(url_for('users.list'))

    elif request.method == 'GET':
        form.user_username.data = user.user_username
        form.user_email.data = user.user_email
        form.user_role.data = user.user_role

    return render_template('edit_user.html', form=form, user_id=user_id)


@users.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.user_role != 'Admin':
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted')
    return redirect(url_for('users.list'))


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get_or_404(current_user.id)

    form = UserProfileForm()
    change_pw_form = ChangePasswordForm()

    if form.validate_on_submit():
        user.user_username = form.user_username.data
        user.user_email = form.user_email.data
        user.user_role = form.user_role.data
        user.user_first_name = form.user_first_name.data
        user.user_last_name = form.user_last_name.data
        # user.user_birthday = form.user_birthday.data
        user.user_location = form.user_location.data
        user.user_about = form.user_about.data
        user.user_occupation = form.user_occupation.data
        user.user_interests = form.user_interests.data

        print(form.submit.label)
        db.session.commit()
        flash('profile Updated')
        return redirect(url_for('conclave.index'))

    elif request.method == 'GET':
        form.user_username.data = user.user_username
        form.user_email.data = user.user_email
        form.user_role.data = user.user_role
        form.user_first_name.data = user.user_first_name
        form.user_last_name.data = user.user_last_name
        # form.user_birthday.data = user.user_birthday
        form.user_location.data = user.user_location
        form.user_about.data = user.user_about
        form.user_occupation.data = user.user_occupation
        form.user_interests.data = user.user_interests

    if change_pw_form.validate_on_submit():
        user.user_password = change_pw_form.new_password.data
        db.session.commit()
        flash('Password Changed', 'success')
        return redirect(url_for('users.profile'))

    return render_template('profile_edit.html', form=form, change_pw_form=change_pw_form)
