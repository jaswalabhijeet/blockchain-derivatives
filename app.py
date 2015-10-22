import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash, Blueprint, \
    send_from_directory, current_app
from flask.ext.sqlalchemy import SQLAlchemy
import psycopg2
import logging
import sys
import uuid
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_wtf import Form
from wtforms import TextField, PasswordField, Form, BooleanField, validators, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)



# in the command line, maybe do: 'run python' and then 'from app import db' and then 'db.create_all()' and to leave: 'exit()'

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '%s %s %s' % (self.email, self.password, self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        # return unicode(self.email)
        return unicode(self.id)

    def is_authenticated(self):
        return True


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
        return '%s  %s  %s  %s  %s  %s  %s  %s  %s' % (
        self.blockchainderivativesid, self.buyerethereumaddress, self.sellerethereumaddress, self.deliverydate,
        self.numberofunits, self.commodityname, self.price, self.margin, self.soliditycodeinitial)

    def __init__(self, blockchainderivativesid, buyerethereumaddress, sellerethereumaddress, deliverydate,
                 numberofunits, commodityname, price, margin, soliditycodeinitial):
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

user = User('email1', 'password2')
db.session.add(user)
db.session.commit()
user = User('email2', 'password2')
db.session.add(user)
db.session.commit()
# all_users = User.query.all()
# print all_users

# contract = Contract('blockchainderivativesid00', 'buyerethereumaddress00', 'sellerethereumaddress00', '1', '1', 'commodityname00', '1', '1', 'soliditycodeinitial00')
# db.session.add(contract)
# db.session.commit()
# all_contracts = Contract.query.all()
# print all_contracts

login_manager = LoginManager()
login_manager.init_app(app)

SECRET_KEY = 'secretkey'
USERNAME = 'username'
PASSWORD = 'password'

class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=1, max=35)])
    password = PasswordField('Password', [validators.Length(min=1, max=35)])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        registered_users = User.query.filter_by(email=form.email.data)
        if registered_users.count() == 0:
            user = User(form.email.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            print 'the user object is:', User.query.get(int(user.id))
            user = User.query.get(int(user.id))
            login_user(user)
            print 'I think you registered and logged in!!'
            return redirect(url_for('index'))
        else:
            print 'Sorry! User with that name'
            return redirect(url_for('login'))  # send to login instead seemed to be a problem with it before
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(Form):
    email = TextField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])  # another option: =[validators.Length(min=1, max=35)])


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        registered_users = User.query.filter_by(
            email=form.email.data)  # add something like this: .filter_by(password=password)
        if registered_users.count() == 1:
            print 'yep, there is a user with that name!!!!'
            user = User.query.filter_by(email=form.email.data).first()
            user = User.query.get(int(user.id))
            login_user(user)
            print 'I think you logged in!!'
            print 'current user id is: ', current_user.id
            if current_user.is_authenticated():
                print 'Current user is authenticated  !!'
            return redirect(url_for("index"))
        else:
            print 'No user with that name'
            return "NO USER WITH THAT NAME"
            return redirect(url_for("register"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
# @app.route('/logout')
@login_required  
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/mycontracts')
@login_required
def mycontracts():
    return render_template('mycontracts.html', contracts=Contract.query.all())  #a good project for tomorrow is adjusting this to just query contracts of logged in user, it might be contracts=Contract.query.filter_by(blockchainderivativesid=current_user.id)


@app.route('/')
def index():
    return render_template('index.html')  # may want to add user=current_user


@app.route('/futureethereum', methods=["GET", "POST"])
@login_required
def main_future():
    error = None
    if request.method == 'POST':
        print request.form['buyerethereumaddress']
        contract = Contract(str(current_user.id), request.form['buyerethereumaddress'],
                            request.form['sellerethereumaddress'], request.form['deliverydate'],
                            request.form['numberofunits'], request.form['commodityname'], request.form['price'],
                            request.form['margin'], request.form['soliditycodeinitial'])  #might not need str()
        db.session.add(contract)
        db.session.commit()
        all_contracts = Contract.query.all()
        print all_contracts
        # if request.form['buyerethereumaddress'] == null:
        # error = 'Invalid buyer ethereum address'
        # elif request.form['sellerethereumaddress'] == null:
        # error = 'Invalid seller ethereum address'              #can add this for all fields later
        return render_template('futureethereum.html')
    return render_template('futureethereum.html', error=error)  # remove .html if something screws up


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
    # port = int(os.environ.get("PORT", 33507))
    # app.run(host='0.0.0.0', port=port)
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.debug = True
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "postgresql://williammarino@localhost/blockchainderivatives"),
        SECRET_KEY='super scret key',
    )
    app.run(port=port, host=host)
