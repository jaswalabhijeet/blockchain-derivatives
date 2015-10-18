import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash, Blueprint, send_from_directory, current_app
from flask.ext.sqlalchemy import SQLAlchemy
#import psycopg2
#import urlparse
#import db
#import urllib
import logging
import sys
import uuid
from collections import defaultdict
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf import Form
from wtforms import TextField, PasswordField, Form, BooleanField, validators
from wtforms.validators import DataRequired

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://williammarino@localhost/blockchainderivatives")

#SQLALCHEMY_DATABASE_URI = "postgresql://williammarino@localhost/blockchainderivatives"
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']   #may need to flip this on for heroku

#the missing ingredient may be this: We then boot up Heroku’s python terminal using Heroku 'run python' and run 'from file_containing_db import db', followed by 'db.create_all()' to create all the tables that we have defined in our models. To exit the python terminal use, 'exit()'. 

db = SQLAlchemy(app)  
#db.create_all()
#print db.get_tables_for_bind()

class User2(db.Model):
    __tablename__ = "users2"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

#class User(db.Model):
    #email = db.Column(db.String(120), unique=True)
    #password = db.Column(db.String(80))

    #def __init__(self, email, password):        #maybe axe all of this second chunk? 
        #self.email = email
        #self.password = password

#if not db.session.query(User).filter(User.email == email).count():
    #reg = User(email)
    #db.session.add(reg)
    #db.session.commit()

#YOU HAVE TO USE models.Result

#from models import User, db   #maybe get rid of db?

#flip some switch 


login_manager = LoginManager()

SECRET_KEY = 'secretkey',
USERNAME='username',
PASSWORD='password',

#me = User('admin', 'admin@example.com')
#db.session.add(me)
#db.session.commit()

class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #registered_users = User.query.filter_by(email=form.email.data)
            #if user.count() == 0:
        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering the email {0}, please log in'.format(email))
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
        #else:
            #flash('The email {0} is already in use.  Please try a new email'.format(email))
            #return redirect(url_for('register'))

#@login_manager.user_loader
#def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    #return User.query.get(user_id)

    #user = User.query.filter_by(id=user_id)
    #if user.count() == 1:
        #return user.one()
    #return None

class LoginForm(Form):
    email = TextField('Email Address', validators=[validators.Length(min=6, max=35)])     #Try ,.Email()] validator later
    password = PasswordField('Password', validators=[validators.Length(min=6, max=35)])

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)   
    if request.method == 'POST' and form.validate():
    #if form.validate_on_submit():

        #user = User.query.filter_by(email=email).filter_by(password=password)
        #if user.count() == 1:

        #registered_users = User.query.filter_by(email=form.email.data)
            #if user.count() == 0:

        user = User(form.email.data, form.password.data)
        #user = User.query.get(form.email.data, form.password.data) #this slightly different than registration has .query.get
        #user.authenticated = True
        #db.session.add(user)  #don not need, right? 
        #db.session.commit()   #don not need, right? 
        #login_user(user, remember=True)
        #return redirect(url_for("index"))
    return render_template("login.html", form=form)
    #return render_template("login.html")

        #user = User.query.filter_by(email=email).filter_by(password=password)
        #if user.count() == 1:
            #login_user(user.one())
            #flash('Welcome back {0}'.format(email))
            #try:
                #next = request.form['next']
                #return redirect(next)
            #except:
                #return redirect(url_for('index'))
        #else:
            #flash('Invalid login')
            #return redirect(url_for('login'))
    #else:
        #return abort(405)

    #error = None
    #if request.method == 'POST':
        #if request.form['email'] != app.config['USERNAME']:
            #error = 'Invalid username'
        #elif request.form['password'] != app.config['PASSWORD']:
            #error = 'Invalid password'
        #else:
            #session['logged_in'] = True
            #flash('You were logged in')
            #return redirect(url_for('index'))
    #return render_template('login.html', error=error)


@app.route("/logout", methods=["GET"])
#@app.route('/logout')
@login_required  #take out?
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    #session.pop('logged_in', None)
    #flash('You were logged out')
    #return redirect(url_for('index'))

#app.config.update(dict(
    #DEBUG=True,
    #SECRET_KEY = 'secretkey',
    #USERNAME='username',
    #PASSWORD='password',
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///db/sql.db'
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#))



#@app.route('/users')
#def users():
  #return render_template('users.html', users = User.query.all())

#@app.route('/user', methods=['POST'])
#def user():
  #if request.method == 'POST':
    #user = User(request.form['email'], request.form['password'])
    #db.session.add(user)
    #db.session.commit()
  #return redirect(url_for('users'))

@app.route('/')
def index():
    return render_template('index.html')   

@app.route('/futureethereum')
def main_future():
    #return render_template('futureethereum.html')  #this was only thing here initially
    #error = None
    #if request.method == 'POST':
        #if request.form['buyerethereumaddress'] == null:
            #error = 'Invalid buyer ethereum address'
        #elif request.form['sellerethereumaddress'] == null:
            #error = 'Invalid seller ethereum address'
        #elif request.form['deliverydate'] == null:
            #error = 'Invalid delivery date'
        #elif request.form['numberofunits'] == null:
            #error = 'Invalid number of units'
        #elif request.form['commodityname'] == null:
            #error = 'Invalid commodity name'
        #elif request.form['price'] == null:
            #error = 'Invalid price'
        #elif request.form['margin'] == null:
            #error = 'Invalid margin'
        #elif request.form['soliditycodeinitial'] == null:
            #error = 'Invalid solidity code initial'
        #else:
            #session['logged_in'] = True
            #flash('Great')
            #__tablename__ = "FuturesContractsCreated"
            #urllib.uses_netloc.append("postgres")
            #url = urllib.parse(os.environ["DATABASE_URL"])
            #con = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
            #con = psycopg2.connect("dbname=test user=postgres") 	
            #cur = con.cursor()
            #cur.execute("INSERT INTO 'FuturesContractsCreated' (blockchainderivativesid,buyerethereumaddress,sellerethereumaddress, deliverydate, numberofunits, commodityname, price, margin, soliditycodeinitial)) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",[app.config['USERNAME'],request.form['buyerethereumaddress'],request.form['sellerethereumaddress'], request.form['deliverydate'], request.form['numberofunits'], request.form['commodityname'], request.form['price'], request.form['margin'], request.form['soliditycodeinitial']])
            #con.commit()
            #cur.close()
            #con.close()
            #return render_template('futureethereum.html')
            #return redirect(url_for('main_future'))
    #return render_template('futureethereum', error=error)
    return render_template('futureethereum.html')

#check out this page if necessary for better forms: http://stackoverflow.com/questions/20837209/flask-wtform-save-form-to-db

@app.route('/calloptionethereum')
def main_call_option():
    return render_template('calloptionethereum.html')

@app.route('/putoptionethereum')
def main_put_option():
    return render_template('putoptionethereum.html')

@app.route('/swapethereum')
def main_swap():
    return render_template('swapethereum.html')

if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='0.0.0.0')   #turn this on later when you go to another server
    #port = int(os.environ.get('PORT', 5001))
    #app.run(host='0.0.0.0', port=port)
    #port = int(os.environ.get("PORT", 33507))
    #app.run(host='0.0.0.0', port=port)
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)
    #db.create_all()