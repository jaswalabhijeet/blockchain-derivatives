import os
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
#from sqlite3 import dbapi2 as sqlite3
#from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
#import psycopg2
#import urlparse
#import db
#import urllib

#DEBUG=True,
#SECRET_KEY = 'secretkey',
#USERNAME='username',
#PASSWORD='password',
#SQLALCHEMY_DATABASE_URI = 'sqlite:///db/sql.db'

app = Flask(__name__)
#app.config.from_object(__name__)

#login_manager = LoginManager(app)
#login_manager.init_app(app)
#login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

#app.config.update(dict(
    #DEBUG=True,
    #SECRET_KEY = 'secretkey',
    #USERNAME='username',
    #PASSWORD='password',
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///db/sql.db'
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#))

#class User(db.Model, UserMixin):
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String)
    #password = db.Column(db.String)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    #def __repr__(self):
        #return '<Name %r>' % self.name

@app.route('/users')
def main_users():
  return render_template('users.html', users = User.query.all())

@app.route('/user', methods=['POST'])
def user():
  if request.method == 'POST':
    u = User(request.form['name'], request.form['email'])
    db.session.add(u)
    db.session.commit()
  return redirect(url_for('main_users'))


#@login_manager.user_loader
#def user_loader(user_id):
    #user = User.query.filter_by(id=user_id)
    #if user.count() == 1:
        #return user.one()
    #return None

#@app.before_first_request
#def init_request():
    #db.create_all()

#@app.route('/secret')
#@login_required
#def secret():
    #return render_template('secret.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = User.query.filter_by(username=username)
        if user.count() == 0:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('login'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('register'))
    else:
        abort(405)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = User.query.filter_by(username=username).filter_by(password=password)
        if user.count() == 1:
            login_user(user.one())
            flash('Welcome back {0}'.format(username))
            try:
                next = request.form['next']
                return redirect(next)
            except:
                return redirect(url_for('index'))
        else:
            flash('Invalid login')
            return redirect(url_for('login'))
    else:
        return abort(405)


#@app.route('/login', methods=['GET', 'POST'])
#def login():
    #error = None
    #if request.method == 'POST':
        #if request.form['username'] != app.config['USERNAME']:
            #error = 'Invalid username'
        #elif request.form['password'] != app.config['PASSWORD']:
            #error = 'Invalid password'
        #else:
            #session['logged_in'] = True
            #flash('You were logged in')
            #return redirect(url_for('main'))
    #return render_template('login.html', error=error)

#@app.route('/logout')
#def logout():
    #session.pop('logged_in', None)
    #flash('You were logged out')
    #return redirect(url_for('main'))

@app.route('/')
#def main():
#def index():
def home():
    return render_template('index.html')   

#@app.route('/robots.txt')
#def robots():
    #res = app.make_response('User-agent: *\nAllow: /')
    #res.mimetype = 'text/plain'
    #return res

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
    db.create_all()