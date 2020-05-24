import os
import io
import requests
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db, bcrypt, mail, login_manager
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flaskapp.forms import LoginForm, RegistrationForm, UpdateAccountForm, UpdateStatusForm
from flaskapp.models import User

@app.route('/')
@app.route('/home')
def homepage_func():
	return render_template('homepage.html',title_from_python="EPD - Home Page")


@app.route('/about')
def about_func():
        return render_template('about.html',title_from_python="About")



@app.route('/login', methods=['GET', 'POST'])
def login_func():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('homepage_func'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user!=None and bcrypt.check_password_hash(user.password, form.password.data):
			# login with rememerbye
			login_user(user, remember = form.remember.data)
			flash('You have been logged in', 'success')
			# if we login with account page
			next_page = request.args.get('next')
			if next_page == None:
				return redirect(url_for('homepage_func'))
			else:
				return redirect(next_page)
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html',title_from_python="Login", form=form)



@app.route('/register', methods=['GET','POST'])
def registration_func():
	if current_user.is_authenticated:
		return redirect(url_for('homepage_func'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created!', 'success')
		return redirect(url_for('login_func'))
	return render_template('register.html',title_from_python="Register Account", form=form)

@app.route('/logout')
def logout_func():
	logout_user()
	return redirect(url_for('homepage_func'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account_func():

	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('account_func'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='Account', form = form)


@app.route('/update_status', methods=['GET', 'POST'])
@login_required
def update_status_func():
	form = UpdateStatusForm()
	if form.validate_on_submit():
		current_user.av_status = form.av_status.data
		db.session.commit()
		flash('Your status has been updated', 'success')
		return redirect(url_for('update_status_func'))
	elif request.method == 'GET':
		form.av_status.data = current_user.av_status
		return render_template('update_status.html',title='Update Status of ',form=form)


@app.route('/person_visited', methods=['GET', 'POST'])
@login_required
def person_visited_func():
	image_file = url_for('static',filename = current_user.image_file)

	from random import random
	# to solve the cache problem - image is not reloation - it used the cache
	image_file = image_file+'?'+str(random())
	#print(image_file)
	return render_template('person_visted.html',title='Persons Visted ', image_file=image_file)


# use localhost:5000/av_status/username and retrive the status
@app.route('/av_status/<username>', methods=['GET'])
def av_status_func(username):
	if request.method == 'GET':
		user = User.query.filter_by(username=username).first()
		if user != None:
			return user.av_status
		else:
			return 'no user'
	else:
                user = User.query.filter_by(username=username).first()
                if user != None:
                        return user.av_status
                else:
                        return 'no user'

# http://localhost:5000/upload_image/user_name/loc=*home*keepgoing*Downloads*three.png

ttuser = ''
@app.route('/upload_image/<username>/loc=<location>', methods=['GET','POST'])
def upload_image_func(username,location):
	global ttuser
	if request.method == 'GET':
		location = location.replace('*','/')
		#print('user is '+username+' location is '+location)

		ttuser=username
		data = open(location,'rb').read()
		r = requests.post('http://localhost:5000/upload_image_2',data=data)
		return 'something '+str(r.status_code)


@app.route('/upload_image_2', methods=['POST'])
def upload_image_2_func():
	global ttuser
	if request.method == 'POST':
		#print('Got image for: '+ttuser)
		picture_path = os.path.join(app.root_path, 'static',ttuser + '.png')
		imageData = request.get_data()
		image = Image.open(io.BytesIO(imageData))
		image.save(picture_path)

		user = User.query.filter_by(username=ttuser).first()
		if user != None:
			user.image_file = ttuser+'.png'
			db.session.commit()
			return 'Uploaded Successfully'
		else:
			return 'no user'
