import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash, Blueprint, send_from_directory, current_app
from flask.ext.sqlalchemy import SQLAlchemy
import psycopg2
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

#the missing ingredient may be this: in the command line, do: 'run python' and then 'from app import db' and then 'db.create_all()' and to leave: 'exit()'

db = SQLAlchemy(app)  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        #return '<Name %r>' % self.name
        #return self.name
        return '%s  %s' % (self.name, self.email)

class Contract(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blockchainderivativesid = db.Column(db.String(64))
    buyerethereumaddress = db.Column(db.String(64))
    sellerethereumaddress = db.Column(db.String(64))
    deliverydate = db.Column(db.Integer)
    numberofunits = db.Column(db.Integer)
    commodityname = db.Column(db.String(64))
    price = db.Column(db.Integer)
    margin = db.Column(db.Integer)
    soliditycodeinitial = db.Column(db.String(64))

    def __repr__(self):
        return '<Price %r>' % self.price
        return '<Margin %r>' % self.margin

    def __init__(self, blockchainderivativesid, buyerethereumaddress, sellerethereumaddress, deliverydate, numberofunits, commodityname, price, margin, soliditycodeinitial):
        self.blockchainderivativesid = blockchainderivativesid
        self.buyerethereumaddress = buyerethereumaddress
        self.sellerethereumaddress = sellerethereumaddress
        self.deliverydate = deliverydate
        self.numberofunits = numberofunits
        self.commodityname = commodityname
        self.price = price
        self.margin = margin
        self.soliditycodeinitial = soliditycodeinitial

db.create_all()

#user = User('John Doe', 'john.doe@example.com')
#db.session.add(user)
#db.session.commit()
#all_users = User.query.all()
#print all_users

#contract = Contract('blockchainderivativesid00', 'buyerethereumaddress00', 'sellerethereumaddress00', '1', '1', 'commodityname00', '1', '1', 'soliditycodeinitial00')
#db.session.add(contract)
#db.session.commit()
#all_contracts = Contract.query.all()
#print all_contracts

#from models import User, db   #maybe get rid of db?

login_manager = LoginManager()

SECRET_KEY = 'secretkey'
USERNAME='username'
PASSWORD='password'
#DEBUG=True

class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':                              #try to add this to the if clause later: and form.validate():
        registered_users = User.query.filter_by(email=form.email.data)
        if registered_users.count() == 0:
            print 'No user with that name'
            user = User(form.email.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            all_users2 = User.query.all()
            print all_users2
        else:
            print 'Sorry! User with that name'
            flash('The email is already in use.  Please try a new email')    
            return redirect(url_for('login'))         #send to login instead seemed to be a problem with it before
    #flash('Thanks for registering the email {0}, please log in'.format(email))
    return render_template('register.html', form=form)

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

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

class LoginForm(Form):
    email = TextField('Email Address', validators=[validators.Length(min=6, max=35)])     #Try ,.Email()] validator later
    password = PasswordField('Password', validators=[validators.Length(min=6, max=35)])

@app.route("/login", methods=["GET", "POST"])
def login():
    #error = None
    form = LoginForm(request.form)   
    if request.method == 'POST':                   #try to add this to the if clause later: and form.validate(): or if form.validate_on_submit():

        registered_users = User.query.filter_by(email=form.email.data) #add something like this: .filter_by(password=password)
        if registered_users.count() == 1:
            print 'there is a user with that name!!!!'
            #login_user(user, remember=True)       #does not work
            #login_user(user.one())
            #session['logged_in'] = True
            flash_errors(form)
            #flash('Welcome back')
            #flash('Welcome back {0}'.format(email))
            #flash(u'Successfully logged in as %s' % form.user.username)
            #user = User(form.email.data, form.password.data)
            #user = User.query.get(form.email.data, form.password.data) #this slightly different than registration has .query.get
            #user.authenticated = True
            return redirect(url_for("index"))
        else: 
            print 'No user with that name'
            #might be a good idea to do an if statement: if password does not line up, do this and if name does not line up, do that
            #error = 'Invalid password'
            #error = 'Invalid username'
            #flash('Invalid login')
            #return redirect(url_for('login'))
            return redirect(url_for("register"))
            #return render_template('login.html', error=error)
    return render_template("login.html", form=form)

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

@app.route('/users')
def users():
  return render_template('users.html', users = User.query.all())

@app.route('/')
def index():
    return render_template('index.html')   

@app.route('/futureethereum', methods=["GET", "POST"])
def main_future():
    error = None
    if request.method == 'POST':
        print request.form['buyerethereumaddress']
        contract = Contract('blockchainderivativesid', request.form['buyerethereumaddress'], request.form['sellerethereumaddress'], request.form['deliverydate'], request.form['numberofunits'], request.form['commodityname'], request.form['1'], request.form['1'], request.form['soliditycodeinitial00')
        #g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    #g.db.commit()
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