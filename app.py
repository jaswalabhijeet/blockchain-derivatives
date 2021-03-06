# imports

import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash, Blueprint, \
    send_from_directory, current_app
import json
from flask.ext.sqlalchemy import SQLAlchemy
import psycopg2
import logging
import sys
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from wtforms import TextField, PasswordField, Form, BooleanField, validators, SubmitField
from wtforms.validators import DataRequired
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from flask_restful import Resource, Api
from decimal import Decimal
from werkzeug.datastructures import ImmutableMultiDict
#pip install mibian, scipy
#import mibian, scipy

# configuration

app = Flask(__name__)
api = Api(app)
app.secret_key = "super secret key"
db = SQLAlchemy(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# database instantiation

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
        try:
            return unicode(self.id)
        except:
            return str(self.id)

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
    transactionid = db.Column(db.String(64))
    spotprice = db.Column(db.Integer)
    soliditycodedeliverydate = db.Column(db.String(64))
    soliditycodecancel = db.Column(db.String(64))

    def __repr__(self):
        return '%s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s' % (
        self.blockchainderivativesid, self.buyerethereumaddress, self.sellerethereumaddress, self.deliverydate,
        self.numberofunits, self.commodityname, self.price, self.margin, self.soliditycodeinitial, self.transactionid, self.spotprice, self.soliditycodedeliverydate, self.soliditycodecancel)

    def __init__(self, blockchainderivativesid, buyerethereumaddress, sellerethereumaddress, deliverydate,
                 numberofunits, commodityname, price, margin, soliditycodeinitial, transactionid, spotprice, soliditycodedeliverydate, soliditycodecancel):
        self.blockchainderivativesid = blockchainderivativesid
        self.buyerethereumaddress = buyerethereumaddress
        self.sellerethereumaddress = sellerethereumaddress
        self.deliverydate = deliverydate
        self.numberofunits = numberofunits
        self.commodityname = commodityname
        self.price = price
        self.margin = margin
        self.soliditycodeinitial = soliditycodeinitial
        self.transactionid = transactionid 
        self.spotprice = spotprice 
        self.soliditycodedeliverydate = soliditycodedeliverydate 
        self.soliditycodecancel = soliditycodecancel 

class Calloption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blockchainderivativesid = db.Column(db.String(64))
    buyerethereumaddress = db.Column(db.String(64))
    sellerethereumaddress = db.Column(db.String(64))
    expirydate = db.Column(db.Integer)
    numberofunits = db.Column(db.Integer)
    assetname = db.Column(db.String(64))
    strikeprice = db.Column(db.Integer)
    premium = db.Column(db.Integer)
    soliditycodeinitial = db.Column(db.String(64))
    soliditycodeexpirydate = db.Column(db.String(64))
    soliditycodecancel = db.Column(db.String(64))

    def __repr__(self):
        return '%s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s' % (
        self.blockchainderivativesid, self.buyerethereumaddress, self.sellerethereumaddress, self.expirydate,
        self.numberofunits, self.assetname, self.strikeprice, self.premium, self.soliditycodeinitial, self.soliditycodeexpirydate, self.soliditycodecancel)

    def __init__(self, blockchainderivativesid, buyerethereumaddress, sellerethereumaddress, expirydate,
                 numberofunits, assetname, strikeprice, premium, soliditycodeinitial, soliditycodeexpirydate, soliditycodecancel):
        self.blockchainderivativesid = blockchainderivativesid
        self.buyerethereumaddress = buyerethereumaddress
        self.sellerethereumaddress = sellerethereumaddress
        self.expirydate = expirydate
        self.numberofunits = numberofunits
        self.assetname = assetname
        self.strikeprice = strikeprice
        self.premium = premium
        self.soliditycodeinitial = soliditycodeinitial
        self.soliditycodeexpirydate = soliditycodeexpirydate
        self.soliditycodecancel = soliditycodecancel

class Putoption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blockchainderivativesid = db.Column(db.String(64))
    buyerethereumaddress = db.Column(db.String(64))
    sellerethereumaddress = db.Column(db.String(64))
    expirydate = db.Column(db.Integer)
    numberofunits = db.Column(db.Integer)
    assetname = db.Column(db.String(64))
    strikeprice = db.Column(db.Integer)
    premium = db.Column(db.Integer)
    soliditycodeinitial = db.Column(db.String(64))
    soliditycodeexpirydate = db.Column(db.String(64))
    soliditycodecancel = db.Column(db.String(64))

    def __repr__(self):
        return '%s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s' % (
        self.blockchainderivativesid, self.buyerethereumaddress, self.sellerethereumaddress, self.expirydate,
        self.numberofunits, self.assetname, self.strikeprice, self.premium, self.soliditycodeinitial, self.soliditycodeexpirydate, self.soliditycodecancel)

    def __init__(self, blockchainderivativesid, buyerethereumaddress, sellerethereumaddress, expirydate,
                 numberofunits, assetname, strikeprice, premium, soliditycodeinitial, soliditycodeexpirydate, soliditycodecancel):
        self.blockchainderivativesid = blockchainderivativesid
        self.buyerethereumaddress = buyerethereumaddress
        self.sellerethereumaddress = sellerethereumaddress
        self.expirydate = expirydate
        self.numberofunits = numberofunits
        self.assetname = assetname
        self.strikeprice = strikeprice
        self.premium = premium
        self.soliditycodeinitial = soliditycodeinitial
        self.soliditycodeexpirydate = soliditycodeexpirydate
        self.soliditycodecancel = soliditycodecancel


class Spotprice(db.Model):
    #__tablename__ = 'spotprice'
    commodity = db.Column(db.String(64), primary_key=True)
    spotprice = db.Column(db.Integer)
    version_id = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        "version_id_col": version_id
    }

    def __repr__(self):
        return '%s  %s' % (
        self.commodity, self.spotprice)

    def __init__(self, commodity, spotprice):
        self.commodity = commodity
        self.spotprice = spotprice

db.create_all()

# registration and log in process and pages

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
    if request.method == 'POST':
        registered_users = User.query.filter_by(email=request.form['email'])
        if registered_users.count() == 0:
            user = User(request.form['email'], request.form['password'])
            db.session.add(user)
            db.session.commit()
            user = User.query.get(int(user.id))
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('There is already a user with that name.')
            return redirect(url_for('login'))
    return render_template('register.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(Form):
    email = TextField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        registered_users = User.query.filter_by(
            email=request.form['email'])
        if registered_users.count() == 1:
            user = User.query.filter_by(email=request.form['email']).first()
            user = User.query.get(int(user.id))
            login_user(user)
            if current_user.is_authenticated():
                pass
            return redirect(url_for("index"))
        else:
            return "NO USER WITH THAT NAME"
            return redirect(url_for("register"))
    return render_template("login.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Must be logged-in for that page.')
    return redirect(url_for('login'))

# pages of website

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/futureethereum', methods=["GET", "POST"])
@login_required
def main_future():
    error = None
    spotprice_dictionary = {}
    for u in Spotprice.query.all():
        dict = u.__dict__
        dict_commodity = dict.get('commodity')
        dict_spotprice = float(dict.get('spotprice'))
        spotprice_dictionary[dict_commodity] = dict_spotprice
    if request.method == 'POST':
        # print current_user.id
        # print request.form['buyerethereumaddress']
        # print request.form['sellerethereumaddress']
        # print request.form['numberofunits']
        # print request.form['commodityname']
        # print request.form['price']
        # print request.form['soliditycodeinitial']
        if ((request.form['buyerethereumaddress'] == '') or (request.form['sellerethereumaddress'] == '') or (request.form['deliverydateTimestamp'] is False) or (request.form['numberofunits'] is False) or (request.form['commodityname'] == '') or (request.form['price'] is False) or (request.form['margin'] is False) or (request.form['soliditycodeinitial'] == '') or (request.form['contractfield2'] == '') or (request.form['contractfield3'] == '')):
            # return redirect(url_for("error"))
            flash('You left a field empty. Please try again.')
            return redirect(url_for('main_future'))
        else:
            contract = Contract(str(current_user.id), request.form['buyerethereumaddress'],
                            request.form['sellerethereumaddress'], request.form['deliverydateTimestamp'],
                            int(request.form['numberofunits']), request.form['commodityname'], request.form['price'],
                            request.form['margin'], request.form['soliditycodeinitial'], 0, 0, request.form['contractfield2'], request.form['contractfield3'])  #might not need str() #change last one or change deliverydate back
            db.session.add(contract)
            db.session.commit()
            return redirect(url_for("mycontracts"))
        #return render_template('futureethereum.html', spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary))
    return render_template('futureethereum.html', error=error, spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary))

@app.route('/calloptionethereum', methods=["GET", "POST"])
@login_required
def main_call_option():
    error = None
    spotprice_dictionary = {}
    for u in Spotprice.query.all():
        dict = u.__dict__
        dict_commodity = dict.get('commodity')
        dict_spotprice = float(dict.get('spotprice'))
        spotprice_dictionary[dict_commodity] = dict_spotprice
    if request.method == 'POST':
        if ((request.form['buyerethereumaddress'] == '') or (request.form['sellerethereumaddress'] == '') or (request.form['expirydateTimestamp'] is False) or (request.form['numberofunits'] is False) or (request.form['assetname'] == '') or (request.form['strikeprice'] is False) or (request.form['premium'] is False) or (request.form['soliditycodeinitial'] == '') or (request.form['contractfield2'] == '') or (request.form['contractfield3'] == '')):
            #return redirect(url_for("error"))
            flash('You left a field empty. Please try again.')
            return redirect(url_for('main_call_option'))
        else:
            print request.form['premium']
            print type(int(request.form['premium']))
            contract = Calloption(str(current_user.id), request.form['buyerethereumaddress'],
                            request.form['sellerethereumaddress'], request.form['expirydateTimestamp'],
                            request.form['numberofunits'], request.form['assetname'], request.form['strikeprice'],
                            int(request.form['premium']), request.form['soliditycodeinitial'], request.form['contractfield2'], request.form['contractfield3'])  #might not need str() #change last one or change deliverydate back
            db.session.add(contract)
            db.session.commit()
            return redirect(url_for("mycontracts"))
            # return render_template('calloptionethereum.html', spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary))
    return render_template('calloptionethereum.html', error=error, spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary)) #spotpricesjson=json.dumps(Spotprice.query.all()))

@app.route('/putoptionethereum', methods=["GET", "POST"])
@login_required
def main_put_option():
    error = None
    spotprice_dictionary = {}
    for u in Spotprice.query.all():
        dict = u.__dict__
        dict_commodity = dict.get('commodity')
        dict_spotprice = float(dict.get('spotprice'))
        spotprice_dictionary[dict_commodity] = dict_spotprice
    if request.method == 'POST':
        if ((request.form['buyerethereumaddress'] == '') or (request.form['sellerethereumaddress'] == '') or (request.form['expirydateTimestamp'] is False) or (request.form['numberofunits'] is False) or (request.form['assetname'] == '') or (request.form['strikeprice'] is False) or (request.form['premium'] is False) or (request.form['soliditycodeinitial'] == '') or (request.form['contractfield2'] == '') or (request.form['contractfield3'] == '')):
            return redirect(url_for("error"))
        else:
            contract = Putoption(str(current_user.id), request.form['buyerethereumaddress'],
                            request.form['sellerethereumaddress'], request.form['expirydateTimestamp'],
                            request.form['numberofunits'], request.form['assetname'], request.form['strikeprice'],
                            int(request.form['premium']), request.form['soliditycodeinitial'], request.form['contractfield2'], request.form['contractfield3'])  #might not need str() #change last one or change deliverydate back
            db.session.add(contract)
            db.session.commit()
            return redirect(url_for("mycontracts"))
            #return render_template('putoptionethereum.html', spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary))
    return render_template('putoptionethereum.html', error=error, spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary)) #spotpricesjson=json.dumps(Spotprice.query.all()))


# @app.route('/swapethereum', methods=["GET", "POST"])
# def main_swap():
#     error = None
#     spotprice_dictionary = {}
#     for u in Spotprice.query.all():
#         dict = u.__dict__
#         dict_commodity = dict.get('commodity')
#         dict_spotprice = float(dict.get('spotprice'))
#         spotprice_dictionary[dict_commodity] = dict_spotprice
#     if request.method == 'POST':
#         contract = Contract(str(current_user.id), request.form['buyerethereumaddress'],
#                             request.form['sellerethereumaddress'], request.form['deliverydateTimestamp'],
#                             request.form['numberofunits'], request.form['commodityname'], request.form['price'],
#                             request.form['margin'], request.form['soliditycodeinitial'], 0, 0, request.form['contractfield2'], request.form['contractfield3'])  #might not need str() #change last one or change deliverydate back
#         db.session.add(contract)
#         db.session.commit()
#         return render_template('swapethereum.html', spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary))
#     return render_template('swapethereum.html', error=error, spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary)) #spotpricesjson=json.dumps(Spotprice.query.all()))

@app.route('/mycontracts')
@login_required
def mycontracts():
    return render_template('mycontracts.html', contracts=Contract.query.all(), calloptions=Calloption.query.all(), putoptions=Putoption.query.all())

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route("/spotprices", methods=["GET", "POST"])   #changed the href here
def spotprices():
    error = None
    if request.method == 'POST':
        spotprice = Spotprice(request.form['commodity'], request.form['spotprice'])
        db.session.add(spotprice)
        db.session.commit()
        return render_template('spotprices.html', spotprices=Spotprice.query.all())
    return render_template('spotprices.html',  error=error, spotprices=Spotprice.query.all())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')

# RESTful API

class SpotpriceApi(Resource):

    def put(self, spotpriceapi):
        commodity_response = request.form['commodity']
        if len(commodity_response) == 0:
            abort(404)
        spotprice_response = request.form['spotprice']
        if len(spotprice_response) == 0:
            abort(404)

        try:
            if type(request.form['commodity']) != unicode:
                abort(400)
        except:
            if type(request.form['commodity']) != str:
                abort(400)

        try:
            if type(request.form['spotprice']) != unicode:
                abort(400)
        except:
            if type(request.form['spotprice']) != str:
                abort(400)

        try :
            spotpricetoupdate = Spotprice.query.filter_by(commodity=request.form['commodity']).first()
            newprice = request.form['spotprice']
            spotpricetoupdate.spotprice = newprice
            db.session.commit()
        except :
            spotprice = Spotprice(request.form['commodity'], request.form['spotprice'])
            db.session.add(spotprice)
            db.session.commit()
        return {}

api.add_resource(SpotpriceApi, '/<string:spotpriceapi>')

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 33507))
    # app.run(host='0.0.0.0', port=port)
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.debug = True
    # app.config.update(
    #     SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "postgresql://williammarino@localhost/blockchainderivatives"),
    #     SECRET_KEY='super scret key',
    # )
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "postgresql://williammarino@localhost/blockchainderivatives"))
    app.run(port=port, host=host)
