import os
import json
import requests
import time
from app import app
import unittest
import tempfile
from flask import jsonify
from flask import url_for

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        #self.app = app.app.test_client()   #turn back on if need be
        #self.app.config['TESTING'] = True  #take out if you have to
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        # db.create_all()

    def test_index_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_future_ethereum_status_code(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/futureethereum')
        try:
            self.assertEqual(result.status_code, 200)
        except:
            self.assertEqual(result.status_code, 302)

    def test_calloption_ethereum_status_code(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/calloptionethereum')
        try:
            self.assertEqual(result.status_code, 200)
        except:
            self.assertEqual(result.status_code, 302)

    def test_putoption_ethereum_status_code(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/putoptionethereum')
        try:
            self.assertEqual(result.status_code, 200)
        except:
            self.assertEqual(result.status_code, 302)

    # def test_swap_ethereum_status_code(self):
    #     result = self.app.get('/swapethereum')
    #     self.assertEqual(result.status_code, 200)

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
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/mycontracts')
        self.assertEqual(result.status_code, 200)

    def test_tutorial_status_code(self):
        result = self.app.get('/tutorial')
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

    # def test_future_post_valid_inputs(self):
    #     self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
    #     self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
    #     response = self.app.post('/futureethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', deliverydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, commodityname='wheat', price=22, margin=2, contractfield='', transactionid='', spotprice=1, contractfield2='', contractfield3=''), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_future_post_missing_inputs(self):
    #     self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
    #     self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
    #     response = self.app.post('/futureethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', deliverydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, commodityname='wheat', price=22, margin=2, contractfield='', transactionid='', spotprice=1, contractfield2=''), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_calloption_post_valid_inputs(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/calloptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='', contractfield2='', contractfield3=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_calloption_post_missing_inputs(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/calloptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='', contractfield2=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_putoption_post_valid_inputs(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='', contractfield2='', contractfield3=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_putoption_post_missing_inputs(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='', contractfield2=''), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_then_login(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_then_login_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        print response
        #self.assertEqual(response.request.path, url_for('index'))
        #self.assertEqual(response.location, url_for('index', _external=True))
        # self.assertEqual(response.location, '/')

    def test_register_then_login_then_logout(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_logout_without_login(self):
        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

#run from command line with: python tests.py
