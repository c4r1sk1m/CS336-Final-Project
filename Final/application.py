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


 
@application.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('loginpage.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"
                   
 
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
    return home()

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



 
if __name__ == "__main__":    
    application.config['SESSION_TYPE'] = 'filesystem'
    # db.create_all()
    application.run(host='0.0.0.0', port=4000)
