from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask import request
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

import os


application  = Flask(__name__)
application.secret_key = "Secret"

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Combat0208!@cs336-spring2018.cxaikb3deay0.us-east-2.rds.amazonaws.com/FinalProject'
db = SQLAlchemy(application)
application.debug = True
##############################This section sets up all the tables in Python so that the RDB can be Queried#######################################
class User(db.Model):
    id = db.Column(db.Integer, unique=True,autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password_hash = pbkdf2_sha256.hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Users(db.Model):
	idusers       = db.Column(db.Integer, unique=True,autoincrement=True, primary_key=True)
	username      = db.Column(db.String(45), unique=True)
	password      = db.Column(db.String(45), unique=True)
	first_name    = db.Column(db.String(45), unique=True)
	last_name     = db.Column(db.String(45), unique=True)
	email_address = db.Column(db.String(45), unique=True)
	def __init__(self,username,password,first_name,last_name,email_address):
		self.username 	   = username
		self.passowrd	   = pbkdf2_sha256.hash(password)
		self.first_name	   = first_name
		self.last_name 	   = last_name
		self.email_address = email_address
	def __repr__(self):
		return '<Users {}>'.format(self.username)


class Bookmarks(db.Model):
	bookmark_id = db.Column(db.Integer,primary_key=True)
	home 		= db.Column(db.Integer)
	user        = db.Column(db.Integer)
	def __init__(bookmark_id,home,user):
		self.bookmark_id=bookmark_id
		self.home=home
		self.user=user
	def __repr__(self):
		return '<Bookmarks {}>'.format(self.bookmark_id)


class Features(db.Model):
	entryid 	 = db.Column(db.Integer,primary_key=True)
	house 		 = db.Column(db.Integer)
	feature_type = db.Column(db.String(30))
	def __init__(entryid,house,feature_type):
		self.entryid=entryid
		self.house=house
		self.feature_type=feature_type
	def __repr__(self):
		return '<Features {}>'.format(self.entryid)


class Home(db.Model):
	hid				= db.Column(db.Integer,primary_key=True)
	address 		= db.Column(db.String(40))
	home_type		= db.Column(db.String(40))
	acres			= db.Column(db.Integer)
	construct_date	= db.Column(db.String(10))
	cost 			= db.Column(db.Float)
	seller 			= db.Column(db.Integer)
	def __init__(hid,address,home_type,acres,construct_date,cost,seller):
		self.hid 			= hid
		self.address     	= address
		self.home_type 		= home_type
		self.acres 			= acres
		self.construct_date = construct_date
		self.cost 			= cost
		self.seller 		= seller
	def __repr__(self):
		return '<Home {}>'.format(self.hid)


class Room(db.Model):
	house		 = db.Column(db.Integer)
	room_type	 = db.Column(db.String(15))
	amount 		 = db.Column(db.Integer)
	entryid		 = db.Column(db.Integer,primary_key=True)
	def __init__(house,room_type,amount,entryid):
		self.house		 = house
		self.room_type	 = room_type
		self.amount		 = amount
		self.entryid	 = entryid
	def __repr__(self):
		return '<Room {}>'.format(self.entryid)

class Seller(db.Model):
	seller_id		= db.Column(db.Integer,primary_key=True)
	phone_num		= db.Column(db.String(12))
	email 			= db.Column(db.String(70))
	seller_fname	= db.Column(db.String(30))
	seller_lname 	= db.Column(db.String(30))
	def __init__(seller_id,phone_num,email,seller_fname,seller_lname):
		self.seller_id 		= seller_id
		self.phone_num 		= phone_num
		self.email 			= email
		self.seller_fname 	= seller_fname
		self.seller_lname 	= seller_lname
	def __repr__(self):
		return '<Seller {}>'.format(self.seller_id)


class Utilities(db.Model):
	entryid 	= db.Column(db.Integer,primary_key=True)
	house 		= db.Column(db.Integer)
	util_type	= db.Column(db.String(15))
	def __init__(entryid,house,util_type):
		self.entryid 	= entryid
		self.house 		= house
		self.util_type  = util_type
	def __repr__(self):
		return '<Utilities {}>'.format(self.entryid)
#################################################################This controls the website routing#################################################################################
 
@application.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('buy.html')
    else:
    	return render_template('properties.html')




@application.route('/signin')
def signIn():
	return render_template('loginpage.html')    	
                   
 
@application.route('/login', methods=['POST'])
def do_admin_login():
    pw        = request.form['password']
    user_name = request.form['username']    
    myUser =  User.query.filter_by(username=user_name).first()
    if(myUser is None):
        flash('Invalid username or password. Please try again!')
    else:
        try:
            if(pbkdf2_sha256.verify(pw,myUser.password_hash)):
                session['logged_in'] = True
                # return render_template('add_user.html')
                return home()
            else:
                flash('Invalid username or password. Please try again!')
        except TypeError:            
            flash('Invalid username or password. Please try again!')
    return render_template('loginpage.html')

@application.route("/signup")
def display():
    return render_template('add_user.html')


@application.route("/sign_up",methods=['POST'])
def sign_up():
    #print(request.form.get('username'))
    username = request.form.get('username')#request.form['username']
    email = request.form.get('email')#request.password['email']
    pw = request.form.get('password')#request.form['password']
    print(username)
    print(email)
    print(pw)
    user = User(username, email, pw)
    db.session.add(user)
    try:
        db.session.commit()
        flash('Sign Up Complete! Login to Continue')
    except IntegrityError:
        flash('User Already Exists. Login to Continue')
    return render_template('add_user.html')
 

@application.route("/logout")
def logout():
    session['logged_in'] = False
    return home()          


@application.route("/rent")
def rent():
	return render_template('rent.html')


@application.route("/buy")
def buy():
	return render_template('buy.html')


@application.route("/properties")
def properties():
	return render_template('properties.html')
 

@application.route("/devtest")
def devtest():
	return render_template('devtest.html')

@application.route("/search")
def search():
	return render_template('search.html')
 


if __name__ == "__main__":    
    application.config['SESSION_TYPE'] = 'filesystem'
    # db.create_all()
    application.run(host='0.0.0.0', port=4000)
