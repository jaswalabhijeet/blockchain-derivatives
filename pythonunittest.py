import os
import json
import requests
import time
from app import app
import unittest
import tempfile
from flask import jsonify

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        #self.app = app.app.test_client()   #turn back on if need be
        #self.app.config['TESTING'] = True  #take out if you have to
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        # db.create_all()

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

#test functional units on pages & check if necessary forms are

    #def test_future_ethereum_status_code(self):
        # sends HTTP GET request to the application, on the Ethereum future page
        #result = self.app.get('/futureethereum') 
        # assert the status code of the response
        #self.assertEqual(result.status_code, 200)

    def test_index_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_future_ethereum_status_code(self):
        result = self.app.get('/futureethereum')
        self.assertEqual(result.status_code, 200)

    def test_calloption_ethereum_status_code(self):
        result = self.app.get('/calloptionethereum')
        self.assertEqual(result.status_code, 200)

    def test_putoption_ethereum_status_code(self):
        result = self.app.get('/putoptionethereum')
        self.assertEqual(result.status_code, 200)

    def test_swap_ethereum_status_code(self):
        result = self.app.get('/swapethereum')
        self.assertEqual(result.status_code, 200)

    def test_register_status_code(self):
        result = self.app.get('/register')
        self.assertEqual(result.status_code, 200)

    def test_login_status_code(self):
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_spotprices_status_code(self):
        result = self.app.get('/spotprices')
        self.assertEqual(result.status_code, 200)

    def test_mycontracts_status_code(self):
        result = self.app.get('/mycontracts')
        self.assertEqual(result.status_code, 200)

    def test_api_valid_data(self):
        response = self.app.put('/spotpriceapi', data=dict(
        commodity='barley',
        spotprice=9.99
    ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_invalid_commodity_data(self):
        response = self.app.put('/spotpriceapi', data=dict(
        commodity='',
        spotprice=9.99
    ), follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_api_invalid_spotprice_data(self):
        response = self.app.put('/spotpriceapi', data=dict(
        commodity='barley',
        spotprice=''
    ), follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_api_invalid_method_get(self):
        response = self.app.get('/spotpriceapi', data=dict(
        commodity='barley',
        spotprice=9.99
    ), follow_redirects=True)
        self.assertEqual(response.status_code, 405)

    def test_api_invalid_method_post(self):
        response = self.app.post('/spotpriceapi', data=dict(
        commodity='barley',
        spotprice=9.99
    ), follow_redirects=True)
        self.assertEqual(response.status_code, 405)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # def test_login_logout(self):
    #     result = self.login('username', 'password')
        #print jsonify(result.headers)
        #self.assertEqual(result.data, index.html)
        # self.assertEqual(result.status_code, 200)
        #session['logged_in']
        #rv = self.login('username', 'password')
        #assert 'You were logged in' in rv.data
        #rv = self.logout()
        #assert 'You were logged out' in rv.data
        #rv = self.login('adminx', 'default')
        #assert 'Invalid username' in rv.data
        #rv = self.login('admin', 'defaultx')
        #assert 'Invalid password' in rv.data

if __name__ == '__main__':
    unittest.main()

#run from command line with: python tests.py
