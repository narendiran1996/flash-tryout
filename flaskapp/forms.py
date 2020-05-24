from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
from flaskapp.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',validators = [DataRequired(), Email()])

	password = PasswordField('Password',validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign up')


	# for unique username and password
	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user!=None:
			print("aiyoo")
			raise ValidationError('Username taken')
	def validate_email(self,email):
                user= User.query.filter_by(email=email.data).first()
                if user!=None:
                        raise ValidationError('Email already used')


class LoginForm(FlaskForm):
	email = StringField('Email',validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',validators = [DataRequired(), Email()])
	submit = SubmitField('Update')
	# for unique username and  email
	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user!=None:
				raise ValidationError('Username taken')
	def validate_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user!=None:
				raise ValidationError('Email already used')

class UpdateStatusForm(FlaskForm):
	av_status = StringField('Status in : ', validators=[DataRequired(), Length(min=2, max=100)])
	submit = SubmitField('Update Status')
