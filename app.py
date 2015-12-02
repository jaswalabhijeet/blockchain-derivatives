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

#html = urlopen("http://www.google.com/")
#print(html.read())

app = Flask(__name__)
api = Api(app)
app.secret_key = "super secret key"

# in the command line, maybe do: 'run python' and then 'from app import db' and then 'db.create_all()' and to leave: 'exit()'

db = SQLAlchemy(app)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


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

# user = User('email1', 'password2')
# db.session.add(user)
# db.session.commit()
# user = User('email2', 'password2')
# db.session.add(user)
# db.session.commit()
# all_users = User.query.all()
# print all_users
# contract = Contract('blockchainderivativesid00', 'buyerethereumaddress00', 'sellerethereumaddress00', '1', '1', 'commodityname00', '1', '1', 'soliditycodeinitial00', '1', '1', '1', '1')
# db.session.add(contract)
# db.session.commit()
# all_contracts = Contract.query.all()
# print all_contracts
# spotprice = Spotprice('wheat', '1.01')
# db.session.add(spotprice)
# db.session.commit()
# spotprice = Spotprice('gold', '1.01')
# db.session.add(spotprice)
# db.session.commit()
# allSpotPrices=Spotprice.query.all()
# print allSpotPrices

login_manager = LoginManager()
login_manager.init_app(app)

SECRET_KEY = 'secretkey'
USERNAME = 'username'
PASSWORD = 'password'

class RegistrationForm(Form):      #possibly not using any more
    email = TextField('Email Address', [validators.Length(min=1, max=35)])
    password = PasswordField('Password', [validators.Length(min=1, max=35)])

@app.route('/register', methods=['GET', 'POST'])
def register():
    # form = RegistrationForm(request.form)
    if request.method == 'POST':
        # registered_users = User.query.filter_by(email=form.email.data)
        registered_users = User.query.filter_by(email=request.form['email'])
        if registered_users.count() == 0:
            # user = User(form.email.data, form.password.data)
            user = User(request.form['email'], request.form['password'])
            db.session.add(user)
            db.session.commit()
            user = User.query.get(int(user.id))
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    # return render_template('register.html', form=form)
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
    # form = LoginForm(request.form)
    if request.method == 'POST':
        # registered_users = User.query.filter_by(
        #     email=form.email.data)
        registered_users = User.query.filter_by(
            email=request.form['email'])
        if registered_users.count() == 1:
            # user = User.query.filter_by(email=form.email.data).first()
            user = User.query.filter_by(email=request.form['email']).first()
            user = User.query.get(int(user.id))
            login_user(user)
            if current_user.is_authenticated():
                pass
            return redirect(url_for("index"))
        else:
            return "NO USER WITH THAT NAME"
            return redirect(url_for("register"))
    # return render_template("login.html", form=form)
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required  
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/mycontracts')
# @login_required
def mycontracts():
    return render_template('mycontracts.html', contracts=Contract.query.all())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/futureethereum', methods=["GET", "POST"])
def main_future():
    error = None
    if request.method == 'POST':
        contract = Contract(str(current_user.id), request.form['buyerethereumaddress'],
                            request.form['sellerethereumaddress'], request.form['deliverydateTimestamp'],
                            request.form['numberofunits'], request.form['commodityname'], request.form['price'],
                            request.form['margin'], request.form['contractfield'], 0, 0, request.form['contractfield2'], request.form['contractfield3'])  #might not need str() #change last one or change deliverydate back 
        db.session.add(contract)
        db.session.commit()
        return render_template('futureethereum.html', spotprices=Spotprice.query.all())
    return render_template('futureethereum.html', error=error, spotprices=Spotprice.query.all())


@app.route('/calloptionethereum', methods=["GET", "POST"])
def main_call_option():
    error = None
    #print Spotprice.query.all()
    # list_of_dictionaries = []
    spotprice_dictionary = {}
    for u in Spotprice.query.all():
        # little_list = []
        dict = u.__dict__
        dict_commodity = dict.get('commodity')
        # little_list.append(dict_commodity)
        dict_spotprice = float(dict.get('spotprice'))
        spotprice_dictionary[dict_commodity] = dict_spotprice
        # little_list.append(dict_spotprice)
        # list_of_dictionaries.append(little_list)
        #list_of_dictionaries(u.__dict__)
    # print list_of_dictionaries
    # print spotprice_dictionary
    if request.method == 'POST':
        contract = Contract(str(current_user.id), request.form['buyerethereumaddress'],
                            request.form['sellerethereumaddress'], request.form['deliverydateTimestamp'],
                            request.form['numberofunits'], request.form['commodityname'], request.form['price'],
                            request.form['margin'], request.form['soliditycodeinitial'], 0, 0, request.form['contractfield2'], request.form['contractfield3'])  #might not need str() #change last one or change deliverydate back
        db.session.add(contract)
        db.session.commit()
        return render_template('calloptionethereum.html', spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary))
    return render_template('calloptionethereum.html', error=error, spotprices=Spotprice.query.all(), spotpriceslist=json.dumps(spotprice_dictionary)) #spotpricesjson=json.dumps(Spotprice.query.all()))


@app.route('/putoptionethereum')
def main_put_option():
    return render_template('putoptionethereum.html')


@app.route('/swapethereum')
def main_swap():
    return render_template('swapethereum.html')

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

class SpotpriceApi(Resource):

    def put(self, spotpriceapi):  #chanted from put
        # newprice = request.form['spotprice']
        # spotpricetoupdate = Spotprice.query.filter_by(commodity=request.form['commodity']).first()
        # spotpricetoupdate.spotprice = newprice
        # db.session.commit()
        if len(commodity=request.form['commodity']) == 0:
            abort(404)
        if len(commodity=request.form['spotprice']) == 0:
            abort(404)
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

#so I think the way to trigger this is to send: curl http://localhost:5000/todo1 -d "data=Remember the milk" -X PUT
#or curl -H 'Content-Type: application/json' -X PUT -d '{"commodity": "naturalgas", "spotprice":1.22}' http://0.0.0.0:8080/spotpriceapi




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
