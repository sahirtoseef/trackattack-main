from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from app import bcrypt, db, app
from app.models import User, Entry
from app.users.forms import (RegistrationForm, LoginForm, RequestResetForm,
                            ResetPasswordForm, EntryForm, ProfileForm)
from app.users.utils import save_picture, send_reset_email
from ast import literal_eval as make_tuple
import datetime

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_pw,
                    full_name=form.full_name.data,
                    age=form.age.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created", "success")
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register an Account", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Failed! Please check your Email and Password", 'danger')
    return render_template("login.html", title="User Login", form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.date_posted.desc()).paginate(page=page, per_page=app.config['PAGINATION_PER_PAGE'])
    return render_template('dashboard.html', entries=entries, title="Dashboard")


@users.route('/dashboard/log/entry', methods=['GET', 'POST'])
@login_required
def log_entry():
    form = EntryForm()
    if form.validate_on_submit():
        combined_date_time = datetime.datetime.combine(form.visited_date.data, form.visited_time.data)
        latlong = make_tuple(form.last_visited_location_lat_long.data)
        entry = Entry(full_name=current_user.full_name,
                        age=current_user.age,
                        last_visited_location=form.last_visited_location.data,
                        visited_date_time=combined_date_time,
                        last_visited_location_lat=latlong[0],
                        last_visited_location_long=latlong[1],
                        covid_status=form.covid_status.data,
                        user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash("Your entry has been created", "success")
        return redirect(url_for('users.dashboard'))
    return render_template('log_entry.html', form=form, title="Log Entry")


@users.route('/dashboard/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = ProfileForm()
    if request.method == "GET":
        form.full_name.data = current_user.full_name
        form.age.data = current_user.age

    if form.validate_on_submit():
        current_user.full_name=form.full_name.data
        current_user.age=form.age.data
        db.session.commit()
        flash("Your profile has information has been saved", "success")
        return redirect(url_for('users.dashboard'))
    return render_template('profile.html', form=form, title="Edit Profile")


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash("Your password has been updated! You are now able to log in with your new password", "success")
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)

