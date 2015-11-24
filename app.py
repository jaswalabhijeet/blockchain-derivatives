import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash, Blueprint, \
    send_from_directory, current_app
import json
import urllib2
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


db.create_all()

user = User('email1', 'password2')
db.session.add(user)
db.session.commit()
user = User('email2', 'password2')
db.session.add(user)
db.session.commit()
# all_users = User.query.all()
# print all_users

contract = Contract('blockchainderivativesid00', 'buyerethereumaddress00', 'sellerethereumaddress00', '1', '1', 'commodityname00', '1', '1', 'soliditycodeinitial00', '1', '1', '1', '1')
db.session.add(contract)
db.session.commit()
#all_contracts = Contract.query.all()
#print all_contracts

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
            #print 'the user object is:', User.query.get(int(user.id))
            user = User.query.get(int(user.id))
            login_user(user)
            #print 'I think you registered and logged in!!'
            return redirect(url_for('index'))
        else:
            #print 'Sorry! User with that name'
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
            #print 'yep, there is a user with that name!!!!'
            user = User.query.filter_by(email=form.email.data).first()
            user = User.query.get(int(user.id))
            login_user(user)
            #print 'I think you logged in!!'
            #print 'current user id is: ', current_user.id
            if current_user.is_authenticated():
                #print 'Current user is authenticated  !!'
                pass
            return redirect(url_for("index"))
        else:
            #print 'No user with that name'
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
        #print request.form['buyerethereumaddress']
        contract = Contract(str(current_user.id), request.form['buyerethereumaddress'],
                            request.form['sellerethereumaddress'], request.form['deliverydateTimestamp'],
                            request.form['numberofunits'], request.form['commodityname'], request.form['price'],
                            request.form['margin'], request.form['contractfield'], 0, 0, request.form['contractfield2'], request.form['contractfield3'])  #might not need str() #change last one or change deliverydate back 
        db.session.add(contract)
        db.session.commit()
        #all_contracts = Contract.query.all()
        #print all_contracts
        # if request.form['buyerethereumaddress'] == null:
        # error = 'Invalid buyer ethereum address'
        # elif request.form['sellerethereumaddress'] == null:
        # error = 'Invalid seller ethereum address'              #can add this for all fields later
        return render_template('futureethereum.html')
    return render_template('futureethereum.html', error=error)  # remove .html if something screws up


@app.route('/calloptionethereum', methods=["GET", "POST"])
def main_call_option():
    return render_template('calloptionethereum.html')


@app.route('/putoptionethereum')
def main_put_option():
    return render_template('putoptionethereum.html')


@app.route('/swapethereum')
def main_swap():
    return render_template('swapethereum.html')

def getSpotPrices():
    spotPrices = []
    barleyResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/BARLEY/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    barleyData = barleyResponse.read()
    barleyDataJSON = json.loads(barleyData)
    spotPriceBarley = ("According to WSJ, the spot price of Barley as of " + str(barleyDataJSON['dataset_data']['data'][0][0]) + " is: " + str(barleyDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceBarley)
    cornResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_C1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    cornData = cornResponse.read()
    cornDataJSON = json.loads(cornData)
    spotPriceCorn = ("According to CBOT, the spot price of Corn as of " + str(cornDataJSON['dataset_data']['data'][0][0]) + " is: " + str(cornDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCorn)
    oatsResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_O1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    oatsData = oatsResponse.read()
    oatsDataJSON = json.loads(oatsData)
    spotPriceOats = ("According to CBOT, the spot price of Oats as of " + str(oatsDataJSON['dataset_data']['data'][0][0]) + " is: " + str(oatsDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceOats)
    riceResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_RR1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    riceData = riceResponse.read()
    riceDataJSON = json.loads(riceData)
    spotPriceRice = ("According to CBOT, the spot price of Rice as of " + str(riceDataJSON['dataset_data']['data'][0][0]) + " is: " + str(riceDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceRice)
    soybeanResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_S1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    soybeanData = soybeanResponse.read()
    soybeanDataJSON = json.loads(soybeanData)
    spotPriceSoybean = ("According to CBOT, the spot price of Soybean as of " + str(soybeanDataJSON['dataset_data']['data'][0][0]) + " is: " + str(soybeanDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceSoybean)
    soybeanMealResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_SM1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    soybeanMealData = soybeanMealResponse.read()
    soybeanMealDataJSON = json.loads(soybeanMealData)
    spotPriceSoybeanMeal = ("According to CBOT, the spot price of Soybean Meal as of " + str(soybeanMealDataJSON['dataset_data']['data'][0][0]) + " is: " + str(soybeanMealDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceSoybeanMeal)
    wheatResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/WHEAT_1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    wheatData = wheatResponse.read()
    wheatDataJSON = json.loads(wheatData)
    spotPricewheat = ("According to WSJ, the spot price of Wheat as of " + str(wheatDataJSON['dataset_data']['data'][0][0]) + " is: " + str(wheatDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPricewheat)
    minnesotaWheatResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/WHEAT_MN/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    minnesotaWheatData = minnesotaWheatResponse.read()
    minnesotaWheatDataJSON = json.loads(minnesotaWheatData)
    spotPriceMinnesotaWheat = ("According to WSJ, the spot price of Minnesota Wheat as of " + str(minnesotaWheatDataJSON['dataset_data']['data'][0][0]) + " is: " + str(minnesotaWheatDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceMinnesotaWheat)
    kansasCityWheatResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/WHEAT_KC/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    kansasCityWheatData = kansasCityWheatResponse.read()
    kansasCityWheatDataJSON = json.loads(kansasCityWheatData)
    spotPriceKansasCityWheat = ("According to WSJ, the spot price of Kansas City Wheat as of " + str(kansasCityWheatDataJSON['dataset_data']['data'][0][0]) + " is: " + str(kansasCityWheatDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceKansasCityWheat)
    chicagoWheatResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_W1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    chicagoWheatData = chicagoWheatResponse.read()
    chicagoWheatDataJSON = json.loads(chicagoWheatData)
    spotPriceChicagoWheat = ("According to CBOT, the spot price of Chicago Wheat as of " + str(chicagoWheatDataJSON['dataset_data']['data'][0][0]) + " is: " + str(chicagoWheatDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceChicagoWheat)
    skimmedMilkResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/MILK/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    skimmedMilkData = skimmedMilkResponse.read()
    skimmedMilkDataJSON = json.loads(skimmedMilkData)
    spotPriceSkimmedMilk = ("According to WSJ, the spot price of Skimmed Milk as of " + str(skimmedMilkDataJSON['dataset_data']['data'][0][0]) + " is: " + str(skimmedMilkDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceSkimmedMilk)
    cheeseResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/CHEESE_BRL/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    cheeseData = cheeseResponse.read()
    cheeseDataJSON = json.loads(cheeseData)
    spotPriceCheese = ("According to WSJ, the spot price of Cheese as of " + str(cheeseDataJSON['dataset_data']['data'][0][0]) + " is: " + str(cheeseDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCheese)
    butterResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/BUTTER/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    butterData = butterResponse.read()
    butterDataJSON = json.loads(butterData)
    spotPriceButter = ("According to WSJ, the spot price of Butter as of " + str(butterDataJSON['dataset_data']['data'][0][0]) + " is: " + str(butterDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceButter)
    liveCattleResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_LC1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    liveCattleData = liveCattleResponse.read()
    liveCattleDataJSON = json.loads(liveCattleData)
    spotPriceLiveCattle = ("According to CME, the spot price of Live Cattle as of " + str(liveCattleDataJSON['dataset_data']['data'][0][0]) + " is: " + str(liveCattleDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceLiveCattle)
    feederCattleResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_FC1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    feederCattleData = feederCattleResponse.read()
    feederCattleDataJSON = json.loads(feederCattleData)
    spotPriceFeederCattle = ("According to CME, the spot price of Feeder Cattle as of " + str(feederCattleDataJSON['dataset_data']['data'][0][0]) + " is: " + str(feederCattleDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceFeederCattle)
    hogsResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_FC1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    hogsData = hogsResponse.read()
    hogsDataJSON = json.loads(hogsData)
    spotPriceHogs = ("According to CME, the spot price of Live Hogs as of " + str(hogsDataJSON['dataset_data']['data'][0][0]) + " is: " + str(hogsDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceHogs)
    woolResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/ODA/PWOOLC_USD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    woolData = woolResponse.read()
    woolDataJSON = json.loads(woolData)
    spotPriceWool = ("According to ODA, the spot price of Wool as of " + str(woolDataJSON['dataset_data']['data'][0][0]) + " is: " + str(woolDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceWool)
    rhodiumResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/JOHNMATT/RHOD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    rhodiumData = rhodiumResponse.read()
    rhodiumDataJSON = json.loads(rhodiumData)
    spotPriceRhodium = ("According to Johnson Matthey, the spot price of Rhodium as of " + str(rhodiumDataJSON['dataset_data']['data'][0][0]) + " is: " + str(rhodiumDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceRhodium)
    goldResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_GC1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    goldData = goldResponse.read()
    goldDataJSON = json.loads(goldData)
    spotPriceGold = ("According to COMEX, the spot price of Gold as of " + str(goldDataJSON['dataset_data']['data'][0][0]) + " is: " + str(goldDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceGold)
    silverResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WORLDBANK/WLD_SILVER/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    silverData = silverResponse.read()
    silverDataJSON = json.loads(silverData)
    spotPriceSilver = ("According to WORLD BANK, the spot price of Silver as of " + str(silverDataJSON['dataset_data']['data'][0][0]) + " is: " + str(silverDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceSilver)
    platinumResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/JOHNMATT/PLAT/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    platinumData = platinumResponse.read()
    platinumDataJSON = json.loads(platinumData)
    spotPricePlatinum = ("According to Johnson Matthey, the spot price of Platinum as of " + str(platinumDataJSON['dataset_data']['data'][0][0]) + " is: " + str(platinumDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPricePlatinum)
    copperResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/COPPER_6/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    copperData = copperResponse.read()
    copperDataJSON = json.loads(copperData)
    spotPriceCopper = ("According to the London Metal Exchange, the spot price of Copper as of " + str(copperDataJSON['dataset_data']['data'][0][0]) + " is: " + str(copperDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCopper)
    palladiumResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/JOHNMATT/PALL/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    palladiumData = palladiumResponse.read()
    palladiumDataJSON = json.loads(palladiumData)
    spotPricePalladium = ("According to the Johnson Matthew, the spot price of Palladium as of " + str(palladiumDataJSON['dataset_data']['data'][0][0]) + " is: " + str(palladiumDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPricePalladium)
    aluminumResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/ALUMINIUM_21/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    aluminumData = aluminumResponse.read()
    aluminumDataJSON = json.loads(aluminumData)
    spotPriceAluminum = ("According to the LME, the spot price of Aluminum as of " + str(aluminumDataJSON['dataset_data']['data'][0][0]) + " is: " + str(aluminumDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceAluminum)
    cobaltResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/COBALT_51/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    cobaltData = cobaltResponse.read()
    cobaltDataJSON = json.loads(cobaltData)
    spotPriceCobalt = ("According to the LME, the spot price of Cobalt as of " + str(cobaltDataJSON['dataset_data']['data'][0][0]) + " is: " + str(cobaltDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCobalt)
    leadResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/LEAD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    leadData = leadResponse.read()
    leadDataJSON = json.loads(leadData)
    spotPriceLead = ("According to WSJ, the spot price of Lead as of " + str(leadDataJSON['dataset_data']['data'][0][0]) + " is: " + str(leadDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceLead)
    molybdenumResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/MOLYBDENUM_56/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    molybdenumData = molybdenumResponse.read()
    molybdenumDataJSON = json.loads(molybdenumData)
    spotPriceMolybdenum = ("According to LME, the spot price of Molybdenum as of " + str(molybdenumDataJSON['dataset_data']['data'][0][0]) + " is: " + str(molybdenumDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceMolybdenum)
    nickelResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/ODA/PNICK_USD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    nickelData = nickelResponse.read()
    nickelDataJSON = json.loads(nickelData)
    spotPriceNickel = ("According to ODA, the spot price of Nickel as of " + str(nickelDataJSON['dataset_data']['data'][0][0]) + " is: " + str(nickelDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceNickel)
    steelResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/STEEL/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    steelData = steelResponse.read()
    steelDataJSON = json.loads(steelData)
    spotPriceSteel = ("According to WSJ, the spot price of Steel as of " + str(steelDataJSON['dataset_data']['data'][0][0]) + " is: " + str(steelDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceSteel)
    tinResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/TIN/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    tinData = tinResponse.read()
    tinDataJSON = json.loads(tinData)
    spotPriceTin = ("According to WSJ, the spot price of Tin as of " + str(tinDataJSON['dataset_data']['data'][0][0]) + " is: " + str(tinDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceTin)
    zincResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/WSJ/ZINC/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    zincData = zincResponse.read()
    zincDataJSON = json.loads(zincData)
    spotPriceZinc = ("According to WSJ, the spot price of Zinc as of " + str(zincDataJSON['dataset_data']['data'][0][0]) + " is: " + str(zincDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceZinc)
    rbobGasolineResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_RB1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    rbobGasolineData = rbobGasolineResponse.read()
    rbobGasolineDataJSON = json.loads(rbobGasolineData)
    spotPriceRBOBGasoline = ("According to NYMEX, the spot price of RBOB Gasoline as of " + str(rbobGasolineDataJSON['dataset_data']['data'][0][0]) + " is: " + str(rbobGasolineDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceRBOBGasoline)
    crudeOilResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_CL1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    crudeOilData = crudeOilResponse.read()
    crudeOilDataJSON = json.loads(crudeOilData)
    spotPriceCrudeOil = ("According to NYMEX, the spot price of Crude Oil as of " + str(crudeOilDataJSON['dataset_data']['data'][0][0]) + " is: " + str(crudeOilDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCrudeOil)
    brentCrudeOilResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_B1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    brentCrudeOilData = brentCrudeOilResponse.read()
    brentCrudeOilDataJSON = json.loads(brentCrudeOilData)
    spotPriceBrentCrudeOil = ("According to ICE, the spot price of Brent Crude Oil as of " + str(brentCrudeOilDataJSON['dataset_data']['data'][0][0]) + " is: " + str(brentCrudeOilDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceBrentCrudeOil)
    gulfCoastGasolineResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/FRED/DGASUSGULF/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    gulfCoastGasolineData = gulfCoastGasolineResponse.read()
    gulfCoastGasolineDataJSON = json.loads(gulfCoastGasolineData)
    spotPriceGulfCoastGasoline = ("According to FRED, the spot price of Gulf Coast Gasoline as of " + str(gulfCoastGasolineDataJSON['dataset_data']['data'][0][0]) + " is: " + str(gulfCoastGasolineDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceGulfCoastGasoline)
    naturalGasResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_NG1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    naturalGasData = naturalGasResponse.read()
    naturalGasDataJSON = json.loads(naturalGasData)
    spotPriceNaturalGas = ("According to NYMEX, the spot price of Natural Gas as of " + str(naturalGasDataJSON['dataset_data']['data'][0][0]) + " is: " + str(naturalGasDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceNaturalGas)
    coalResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/ODA/PCOALAU_USD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    coalData = coalResponse.read()
    coalDataJSON = json.loads(coalData)
    spotPriceCoal = ("According to ODA, the spot price of Coal as of " + str(coalDataJSON['dataset_data']['data'][0][0]) + " is: " + str(coalDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCoal)
    arabicaCoffeeResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/ODA/PCOFFOTM_USD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    arabicaCoffeeData = arabicaCoffeeResponse.read()
    arabicaCoffeeDataJSON = json.loads(arabicaCoffeeData)
    spotPriceArabicaCoffee = ("According to ODA, the spot price of Arabica Coffee as of " + str(arabicaCoffeeDataJSON['dataset_data']['data'][0][0]) + " is: " + str(arabicaCoffeeDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceArabicaCoffee)
    robustaCoffeeResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/ODA/PCOFFROB_USD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    robustaCoffeeData = robustaCoffeeResponse.read()
    robustaCoffeeDataJSON = json.loads(robustaCoffeeData)
    spotPriceRobustaCoffee = ("According to ODA, the spot price of Robusta Coffee as of " + str(robustaCoffeeDataJSON['dataset_data']['data'][0][0]) + " is: " + str(robustaCoffeeDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceRobustaCoffee)
    coffeeResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_KC1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    coffeeData = coffeeResponse.read()
    coffeeDataJSON = json.loads(coffeeData)
    spotPriceCoffee = ("According to ICE, the spot price of Coffee as of " + str(coffeeDataJSON['dataset_data']['data'][0][0]) + " is: " + str(coffeeDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCoffee)
    cocoaResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_CC1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    cocoaData = cocoaResponse.read()
    cocoaDataJSON = json.loads(cocoaData)
    spotPriceCocoa = ("According to ICE, the spot price of Cocoa as of " + str(cocoaDataJSON['dataset_data']['data'][0][0]) + " is: " + str(cocoaDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCocoa)
    sugar11Response = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_CC1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    sugar11Data = sugar11Response.read()
    sugar11DataJSON = json.loads(sugar11Data)
    spotPriceSugar11 = ("According to ICE, the spot price of Sugar No. 11 as of " + str(sugar11DataJSON['dataset_data']['data'][0][0]) + " is: " + str(sugar11DataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceSugar11)
    orangeJuiceResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_OJ1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    orangeJuiceData = orangeJuiceResponse.read()
    orangeJuiceDataJSON = json.loads(orangeJuiceData)
    spotPriceOrangeJuice = ("According to ICE, the spot price of Orange Juice as of " + str(orangeJuiceDataJSON['dataset_data']['data'][0][0]) + " is: " + str(orangeJuiceDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceOrangeJuice)
    palmOilResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/ODA/PPOIL_USD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    palmOilData = palmOilResponse.read()
    palmOilDataJSON = json.loads(palmOilData)
    spotPricePalmOil = ("According to ODA, the spot price of Palm Oil as of " + str(palmOilDataJSON['dataset_data']['data'][0][0]) + " is: " + str(palmOilDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPricePalmOil)
    lumberResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_LB1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    lumberData = lumberResponse.read()
    lumberDataJSON = json.loads(lumberData)
    spotPriceLumber = ("According to CME, the spot price of Lumber as of " + str(lumberDataJSON['dataset_data']['data'][0][0]) + " is: " + str(lumberDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceLumber)
    rubberResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/ODA/PRUBB_USD/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    rubberData = rubberResponse.read()
    rubberDataJSON = json.loads(rubberData)
    spotPriceRubber = ("According to CME, the spot price of Rubber as of " + str(rubberDataJSON['dataset_data']['data'][0][0]) + " is: " + str(rubberDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceRubber)
    cottonResponse = urllib2.urlopen('http://www.quandl.com/api/v3/datasets/OFDP/FUTURE_CT1/data.json?api_key=vpiAmDEqu8LuxCupy7ab')
    cottonData = cottonResponse.read()
    cottonDataJSON = json.loads(cottonData)
    spotPriceCotton = ("According to ICE, the spot price of Cotton No. 2 as of " + str(cottonDataJSON['dataset_data']['data'][0][0]) + " is: " + str(cottonDataJSON['dataset_data']['data'][0][1]))
    spotPrices.append(spotPriceCotton)

    return spotPrices
 
@app.route("/spotprices")
def spotprices():
    spotPrices = getSpotPrices()
    return render_template('spotprices.html',**locals())  


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
