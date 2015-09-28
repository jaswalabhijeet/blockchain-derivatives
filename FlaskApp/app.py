from flask import Flask, render_template, request, session, g, redirect, url_for
#from flask.ext.sqlalchemy import SQLAlchemy

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#set up our app
app = Flask(__name__)

#configure our SQLAlchemy DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)

#set up a class for user database
#class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)        #defines a column called id
    #username = db.Column(db.String(80), unique=True)    #defines a column called username
    #email = db.Column(db.String(120), unique=True)      #defines a column called email

    #def __init__(self, username, email):
        #self.username = username
        #self.email = email

    #def __repr__(self):
        #return '<User %r>' % self.username

#when the user comes to the main page, send them to the index template
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/futureethereum')
def main_future():
    return render_template('futureethereum.html')

@app.route('/optionethereum')
def main_option():
    return render_template('optionethereum.html')

@app.route('/swapethereum')
def main_swap():
    return render_template('swapethereum.html')

#we will use this to add the info of a new user to the DB:
#new_user = User('admin', 'admin@example.com')
#db.session.add(new_user)
#db.session.commit()

if __name__ == '__main__':
    app.run()