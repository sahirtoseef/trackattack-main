from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (StringField, SubmitField, PasswordField,
					BooleanField, IntegerField, SelectField,
					HiddenField, DateField, TimeField)
from wtforms.widgets.html5 import NumberInput, DateInput, TimeInput
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
	username = StringField("Username",
						   validators=[DataRequired(), Length(min=2,max=15)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password",
									 validators=[DataRequired(),
												 EqualTo('password', message="Password must be matched!")])
	full_name = StringField("Full Name",
						   validators=[DataRequired(message="This field is required!"), Length(min=2,max=30)])
	age = IntegerField("Age", validators=[DataRequired()], widget=NumberInput())
	
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username already exists! Try choosing another")
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already exists! Try choosing another")

class LoginForm(FlaskForm):
	email = StringField("Email",
						validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")


class EntryForm(FlaskForm):
	visited_date = DateField(widget=DateInput(), validators=[DataRequired()])
	visited_time = TimeField(widget=TimeInput(), validators=[DataRequired()])
	covid_status = SelectField("Covid Status", validators=[DataRequired()], choices=[(2, 'Tested Positive'), (1, 'Have Symptoms'), (0, 'I\'m not sure')])
	last_visited_location = StringField("Last Visited Location", render_kw={'readonly':''}, validators=[DataRequired(message="This field is required!")])
	last_visited_location_lat_long = HiddenField()
	submit = SubmitField("Submit")


class ProfileForm(FlaskForm):
	full_name = StringField("Full Name",
						   validators=[DataRequired(message="This field is required!"), Length(min=2,max=30)])
	age = IntegerField("Age", validators=[DataRequired()], widget=NumberInput())
	submit = SubmitField("Save")


class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Continue")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError("There is no account associated with that email!")

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password",
									 validators=[DataRequired(),
												 EqualTo('password')])
	submit = SubmitField("Reset Password")
