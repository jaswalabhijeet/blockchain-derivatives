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
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_wtf import Form
from wtforms import TextField, PasswordField, Form, BooleanField, validators
from wtforms.validators import DataRequired

from models import User, db   #maybe get rid of db?

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

login_manager = LoginManager()

SECRET_KEY = 'secretkey',
USERNAME='username',
PASSWORD='password',

#db = SQLAlchemy(app)  #removed because redundant? 

class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

    #elif request.method == 'POST':
        #email = request.form['email']
        #password = request.form['password']

        #user = User.query.filter_by(email=email)
        #if user.count() == 0:
            #user = User(email=email, password=password)
            #db.session.add(user)
            #db.session.commit()

            #flash('You have registered the email {0}. Please login'.format(email))
            #return redirect(url_for('login'))
        #else:
            #flash('The email {0} is already in use.  Please try a new email.’.format(email))
            #return redirect(url_for('register'))
    #else:
        #abort(405)

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
    form = LoginForm()
    #if form.validate_on_submit():
        #user = User.query.get(form.email.data)
        #if user:
            #user.authenticated = True
            #db.session.add(user)
            #db.session.commit()
            #login_user(user, remember=True)
            #return redirect(url_for("index"))
    return render_template("login.html", form=form)
    #return render_template("login.html")

    #if request.method == 'GET':
        #return render_template('login.html', next=request.args.get('next'))
    #elif request.method == 'POST':
        #email = request.form['email']
        #password = request.form['password']

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

#class User(db.Model, UserMixin):
    #email = db.Column(db.String)
    #password = db.Column(db.String)

#class User(db.Model):
    #email = db.Column(db.String(120), unique=True)
    #password = db.Column(db.String(80))

    #def __init__(self, email, password):        #maybe axe all of this second chunk? 
        #self.email = email
        #self.password = password

#@app.route('/users')
#def users():
  #return render_template('users.html', users = User.query.all())

#@app.route('/user', methods=['POST'])
#def user():
  #if request.method == 'POST':
    #u = User(request.form['name'], request.form['email'])
    #db.session.add(u)
    #db.session.commit()
  #return redirect(url_for('users'))

#@app.before_first_request
#def init_request():
    #db.create_all()

#@app.route('/secret')
#@login_required
#def secret():
    #return render_template('secret.html')

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
        #elif request.form['seller ethereum address'] == null:
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