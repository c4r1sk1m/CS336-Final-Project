from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask import request
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from sqlalchemy.sql import func

import os


application  = Flask(__name__)
application.secret_key = "Secret"

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Combat0208!@cs336-spring2018.cxaikb3deay0.us-east-2.rds.amazonaws.com/FinalProject'
db = SQLAlchemy(application)
application.debug = True
db.Model.metadata.reflect(db.engine)
##############################This section sets up all the tables in Python so that the RDB can be Queried#######################################

# class User(db.Model):
# 	__table__ = db.Model.metadata.tables['user']
# 	def __init__(self,username,email,password):
# 		self.username = username
# 		self.email = email
# 		self.password_hash = pbkdf2_sha256.hash(password)
# 	def __repr__(self):
# 		return '<User {}>'.format(self.username)


class Users(db.Model):
	__table__ = db.Model.metadata.tables['users']
	def __init__(self,username,password,first_name,last_name,email_address,phone_number):
		self.username 	   = username
		self.password	   = pbkdf2_sha256.hash(password)
		self.first_name	   = first_name
		self.last_name 	   = last_name
		self.email_address = email_address
		self.phone_number  = phone_number
	def __repr__(self):
		return 'Username  :{} \t First Name :{}\t Last Name :{}\t Email Address :{}\t Phone Number :{}'.format(self.username,self.first_name,self.last_name,self.email_address,self.phone_number)



class Home(db.Model):
	__table__ = db.Model.metadata.tables['Home']
	def __init__(self,hid,address,home_type,acres,construct_date,cost,seller):
		self.hid 			= hid
		self.address	 	= address
		self.home_type 		= home_type
		self.acres 			= acres
		self.construct_date = construct_date
		self.cost 			= cost
		self.seller 		= seller
	def __repr__(self):
		return 'Home {},{},{},{},'.format(self.hid,self.address,self.home_type,self.construct_date)



class Bookmarks(db.Model):
	__table__ = db.Model.metadata.tables['Bookmarks']
	def __init__(self,home,user,bookmark_id):
		self.bookmark_id=bookmark_id
		self.home=home
		self.user=user    



class Room(db.Model):
	__table__ = db.Model.metadata.tables['Room']
	def __init__(house,amount):
		self.house		 = house
		self.amount		 = amount





#################################################################This controls the website routing#################################################################################

userID = None

 
@application.route("/")
def home():
	if not session.get('logged_in'):
		return render_template('buy.html', first = [Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first(),
													Home.query.order_by(func.random()).first()])
	else:
		return render_template('properties.html')

@application.route('/signin')
def signIn():
	return render_template('loginpage.html')		
				   
 
@application.route('/login', methods=['POST'])
def do_admin_login():
	pw		= request.form['password']
	user_name = request.form['username']	
	myUser =  Users.query.filter_by(username=user_name).first()
	userID = myUser.idusers
	if(user_name == "admin"):
		session['isAdmin'] = True
		print "is an admin"


	print userID
	if(myUser is None):
		flash('Invalid username or password. Please try again!')
		print 'lol'
	else:
		try:
			if(pbkdf2_sha256.verify(pw,myUser.password)):
				session['logged_in'] = True
				session['myUserID'] = myUser.idusers
				print 'working'
				flash('Login Successful')
				# return render_template('add_user.html')				
			else:
				flash('Invalid username or password. Please try again!')
			# if(myUser.seller == True):
			# 	session['seller'] = True
		except TypeError:			
			flash('Invalid username or password. Please try again!')
	return render_template('loginpage.html')

@application.route("/signup")
def display():
	return render_template('add_user.html')

@application.route("/contact/<int:hid>")
def contact(hid):
	house = Home.query.filter_by(hid=hid).first()
	address = house.address
	sID = house.seller
	seller = Users.query.filter_by(idusers=sID).first()
	s_name = seller.first_name +" "+seller.last_name
	s_email = seller.email_address
	s_phone = seller.phone_number
	print sID


	# pull seller data by HID
	# store into variable
	# pass variable into 
	return render_template('contact.html', house=hid,seller_info= [s_name,s_email,s_phone,address])

@application.route("/settings")
def settings():
	myInfo = Users.query.filter_by(idusers=session['myUserID']).all()
	allInfo = Users.query.all()

	isAdmin = False
	if(session['myUserID'] == 'admin'):
		isAdmin = True
		session['isAdmin'] = True
	return render_template('settings.html',your_list=myInfo,isAdmin=isAdmin,allInfo=allInfo)	


@application.route("/sign_up",methods=['POST'])
def sign_up():
	#print(request.form.get('username'))
	fname 		= request.form.get('fName')
	lname  	 	= request.form.get('lName')
	seller 		= request.form.get('seller')
	username 	= request.form.get('username')#request.form['username']
	email 		= request.form.get('email')#request.password['email']
	pw 			= request.form.get('password')#request.form['password']
	phone 		= request.form.get('pnumber')
	# print(username)
	# print(email)
	# print(pw)
   # (self,username,password,first_name,last_name,email_address):
	user = Users(username,pw,fname,lname,email,phone)
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


# @application.route("/rent")
# def rent():
# 	return render_template('rent.html')


# @application.route("/buy")
# def buy():
# 	return render_template('buy.html')
 

@application.route("/properties")
def properties():
	allProperties = Home.query.all()
	roomCount = list()
	for house in allProperties:
		try:	
			roomCount.append(Room.query.filter_by(house=house.hid).first().amount)
		except AttributeError:
			print 'Not Found'
	return render_template('properties.html', your_list=zip(allProperties,roomCount ))	
#######################################################################
@application.route("/year")
def year():
	allProperties = Home.query.order_by(Home.construct_date).all()
	roomCount = list()
	for house in allProperties:
		try:	
			roomCount.append(Room.query.filter_by(house=house.hid).first().amount)
		except AttributeError:
			print 'Not Found'
	return render_template('properties.html', your_list=zip(allProperties,roomCount ))	

@application.route("/acres")
def acres():
	allProperties = Home.query.order_by(Home.acres).all()
	roomCount = list()
	for house in allProperties:
		try:	
			roomCount.append(Room.query.filter_by(house=house.hid).first().amount)
		except AttributeError:
			print 'Not Found'
	return render_template('properties.html', your_list=zip(allProperties,roomCount ))	

@application.route("/cost")
def cost():
	allProperties = Home.query.order_by(Home.cost).all()
	roomCount = list()
	for house in allProperties:
		try:	
			roomCount.append(Room.query.filter_by(house=house.hid).first().amount)
		except AttributeError:
			print 'Not Found'
	return render_template('properties.html', your_list=zip(allProperties,roomCount ))	

@application.route("/rent")
def rent():
	homeone = Home.query.order_by(func.random()).first()
	houseid = homeone.hid
	roomone = Room.query.filter_by(house=houseid).all()
	
	hometwo = Home.query.order_by(func.random()).first()
	houseid = hometwo.hid
	roomtwo = Room.query.filter_by(house=houseid).all()
	
	homethr = Home.query.order_by(func.random()).first()
	houseid = homethr.hid
	roomthr = Room.query.filter_by(house=houseid).all()
	
	homefou = Home.query.order_by(func.random()).first()
	houseid = homefou.hid
	roomfou = Room.query.filter_by(house=houseid).all()
	
	homefiv = Home.query.order_by(func.random()).first()
	houseid = homefiv.hid
	roomfiv = Room.query.filter_by(house=houseid).all()

	homesix = Home.query.order_by(func.random()).first()
	houseid = homesix.hid
	roomsix = Room.query.filter_by(house=houseid).all()
	
	homesev = Home.query.order_by(func.random()).first()
	houseid = homesev.hid
	roomsev = Room.query.filter_by(house=houseid).all()
	
	homeeig = Home.query.order_by(func.random()).first()
	houseid = homeeig.hid
	roomeig = Room.query.filter_by(house=houseid).all()
	
	homenin = Home.query.order_by(func.random()).first()
	houseid = homenin.hid
	roomnin = Room.query.filter_by(house=houseid).all()
	
	hometen = Home.query.order_by(func.random()).first()
	houseid = hometen.hid
	roomten = Room.query.filter_by(house=houseid).all()
	
	homeele = Home.query.order_by(func.random()).first()
	houseid = homeele.hid
	roomele = Room.query.filter_by(house=houseid).all()
	
	hometwe = Home.query.order_by(func.random()).first()
	houseid = hometwe.hid
	roomtwe = Room.query.filter_by(house=houseid).all()
	return render_template('rent.html',first = [homeone, hometwo, homethr, homefou, homefiv, homesix,
												homesev, homeeig, homenin, hometen, homeele, hometwe],
									   second = [roomone, roomtwo, roomthr, roomfou, roomfiv, roomsix,
												 roomsev, roomeig, roomnin, roomten, roomele, roomtwe])


@application.route("/buy")
def buy():
	homeone = Home.query.order_by(func.random()).first()
	houseid = homeone.hid
	roomone = Room.query.filter_by(house=houseid).all()
	
	hometwo = Home.query.order_by(func.random()).first()
	houseid = hometwo.hid
	roomtwo = Room.query.filter_by(house=houseid).all()
	
	homethr = Home.query.order_by(func.random()).first()
	houseid = homethr.hid
	roomthr = Room.query.filter_by(house=houseid).all()
	
	homefou = Home.query.order_by(func.random()).first()
	houseid = homefou.hid
	roomfou = Room.query.filter_by(house=houseid).all()
	
	homefiv = Home.query.order_by(func.random()).first()
	houseid = homefiv.hid
	roomfiv = Room.query.filter_by(house=houseid).all()

	homesix = Home.query.order_by(func.random()).first()
	houseid = homesix.hid
	roomsix = Room.query.filter_by(house=houseid).all()
	
	homesev = Home.query.order_by(func.random()).first()
	houseid = homesev.hid
	roomsev = Room.query.filter_by(house=houseid).all()
	
	homeeig = Home.query.order_by(func.random()).first()
	houseid = homeeig.hid
	roomeig = Room.query.filter_by(house=houseid).all()
	
	homenin = Home.query.order_by(func.random()).first()
	houseid = homenin.hid
	roomnin = Room.query.filter_by(house=houseid).all()
	
	hometen = Home.query.order_by(func.random()).first()
	houseid = hometen.hid
	roomten = Room.query.filter_by(house=houseid).all()
	
	homeele = Home.query.order_by(func.random()).first()
	houseid = homeele.hid
	roomele = Room.query.filter_by(house=houseid).all()
	
	hometwe = Home.query.order_by(func.random()).first()
	houseid = hometwe.hid
	roomtwe = Room.query.filter_by(house=houseid).all()
	return render_template('buy.html',first = [homeone, hometwo, homethr, homefou, homefiv, homesix,
												homesev, homeeig, homenin, hometen, homeele, hometwe],
									   second = [roomone, roomtwo, roomthr, roomfou, roomfiv, roomsix,
												 roomsev, roomeig, roomnin, roomten, roomele, roomtwe])




@application.route("/house")
def house():
    allProperties = Home.query.filter_by(home_type='House').all()
    return render_template('trends.html', your_list=allProperties)
                           
@application.route("/apartment")
def apartment():
    allProperties = Home.query.filter_by(home_type='Apartment').all()
    return render_template('trends.html', your_list=allProperties)
                           
@application.route("/condo")
def condo():
    allProperties = Home.query.filter_by(home_type='Condo').all()
    return render_template('trends.html', your_list=allProperties)
@application.route("/priceold")
def priceold():
    allProperties = Home.query.filter(Home.construct_date<1980).order_by(Home.cost).all()
    return render_template('trends.html', your_list=allProperties)
@application.route("/pricenew")
def pricenew():
    allProperties = Home.query.filter(Home.construct_date>=1980).order_by(Home.cost).all()
    return render_template('trends.html', your_list=allProperties)
@application.route("/acressmall")
def acressmall():
    allProperties = Home.query.filter(Home.acres<2).all()
    return render_template('trends.html', your_list=allProperties)
@application.route("/acresbig")
def acresbig():
    allProperties = Home.query.filter(Home.acres>3).all()
    return render_template('trends.html', your_list=allProperties)

@application.route("/add_property")
def addProp():
	return render_template('/add_home.html');

@application.route("/add",methods=['POST'])
def add():
	hid = 9999
	address 		= request.form.get('address')
	home_type 		= request.form.get('type')
	acres 			= request.form.get('acres')
	cost 			= request.form.get('cost')
	construct_date 	= request.form.get('date')
	home = Home(hid,address,home_type,acres,construct_date,cost,userID)
	db.session.add(home)
	try:
		db.session.commit()
		flash('Property Successfully Listed')
	except IntegrityError:
		flash('Property Already Exists. Please Enter a new Property.')
	return render_template('add_home.html')

@application.template_global(name='zip')
def _zip(*args, **kwargs): #to not overwrite builtin zip in globals
	return __builtins__.zip(*args, **kwargs)

@application.route("/devtest")
def devtest():
	return render_template('devtest.html')

@application.route("/myhomes")
def myhomes():
	allBookmarks = Home.query.join(Bookmarks).filter_by(user=session['myUserID']).all()
	myHomes = list()
	roomCount = list()
	print len(allBookmarks)
	for bookMark in allBookmarks:
		
		roomCount.append(Room.query.filter_by(house=bookMark.hid).first().amount)

	return render_template('search.html',allBookmarks=allBookmarks,allBookmarked_rooms=zip(allBookmarks,roomCount))
@application.route("/search/<int:hid>")
def search(hid):
	if not session.get('logged_in'):
			return render_template('loginpage.html')
	else:
			bookmark = Bookmarks(hid,session['myUserID'],None)
			db.session.add(bookmark)
			db.session.commit()
			return render_template('search.html', allBookmarks=Home.query.join(Bookmarks).filter_by(user=session['myUserID']).all())
	return render_template('search.html')

if __name__ == "__main__":	
	application.config['SESSION_TYPE'] = 'filesystem'
	application.config['SQLALCHEMY_ECHO'] = True
	#db.create_all()
	application.run(host='0.0.0.0', port=4000)
