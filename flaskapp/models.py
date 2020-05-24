

from datetime import datetime
from flaskapp import db, app, login_manager
from flask_login import UserMixin

# for email verification and reset passowrd
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Extention for login to work

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))




# models - tables

# user table
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120),unique=True, nullable=False)
	av_status = db.Column(db.String(100), default='You have not updated' ,nullable=False )

	image_file = db.Column(db.String(20), default='default.jpg' ,nullable=False )

	password = db.Column(db.String(60), nullable=False)

	#posts = db.relationship('Post', backref='author', lazy=True)

	#printing
	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.av_status}', '{self.image_file})"

	'''
	def  get_reset_token(self, expires_sec = 1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id' : self.id}).decode('utf-8')

	# not using self for self method
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)
	'''
'''
# posts tbale
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	#use current time
	date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	content = db.Column(db.Text, nullable=False)
	# relate post with user -- usermodel -- table and column name - so lower case
	user_id	= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

'''
