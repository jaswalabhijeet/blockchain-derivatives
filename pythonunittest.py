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

    def test_future_ethereum_status_code_loggedin(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/futureethereum')
        try:
            self.assertEqual(result.status_code, 200)
        except:
            self.assertEqual(result.status_code, 302)

    def test_future_ethereum_status_code_loggedout_status(self):
        result = self.app.get('/futureethereum')
        self.assertEquals(result.status_code, 400)

    def test_future_ethereum_status_code_loggedout_redirect(self):
        result = self.app.get('/futureethereum')
        self.assertIn('You should be redirected automatically to target URL', result.data)

    def test_calloption_ethereum_status_code_loggedin(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/calloptionethereum')
        try:
            self.assertEqual(result.status_code, 200)
        except:
            self.assertEqual(result.status_code, 302)

    def test_calloption_ethereum_status_code_loggedout_status(self):
        result = self.app.get('/calloptionethereum')
        print result.data
        try:
            self.assertEqual(result.status_code, 200)
        except:
            self.assertEqual(result.status_code, 302)

    def test_calloption_ethereum_status_code_loggedout_redirect(self):
        result = self.app.get('/calloptionethereum')
        self.assertIn('You should be redirected automatically to target URL', result.data)

    def test_putoption_ethereum_status_code_loggedin(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/putoptionethereum')
        try:
            self.assertEqual(result.status_code, 200)
        except:
            self.assertEqual(result.status_code, 302)

    def test_putoption_ethereum_status_code_loggedout_status(self):
        result = self.app.get('/putoptionethereum')
        self.assertEquals(result.status_code, 400)

    def test_putoption_ethereum_status_code_loggedout_redirect(self):
        result = self.app.get('/putoptionethereum')
        self.assertIn('You should be redirected automatically to target URL', result.data)

    # def test_swap_ethereum_status_code(self):
    #     result = self.app.get('/swapethereum')
    #     self.assertEqual(result.status_code, 200)

    def test_error_status_code(self):
        result = self.app.get('/error')
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

    def test_mycontracts_status_code_loggedin(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        result = self.app.get('/mycontracts')
        self.assertEqual(result.status_code, 200)

    def test_mycontracts_status_code_loggedout_redirect(self):
        result = self.app.get('/mycontracts')
        self.assertIn('You should be redirected automatically to target URL:', result.data)

    def test_mycontracts_status_code_loggedout_status(self):
        result = self.app.get('/mycontracts')
        self.assertEqual(result.status_code, 200)

    def test_tutorial_status_code(self):
        result = self.app.get('/tutorial')
        self.assertEqual(result.status_code, 200)

    def test_unexisting_page(self):
        #result = self.app.get('/SomePage', status=404)
        result = self.app.get('/SomePage')
        # result = self.testapp.get('/SomePage')
        #self.assertTrue(b'Not Found' in result.body)
        # self.assertIn('Not Found', result.data)
        self.assertEqual(result.status_code, 404)

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

    def test_future_post_valid_inputs_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/futureethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', deliverydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, commodityname='wheat', price=22, margin=2, soliditycodeinitial='a', transactionid='', spotprice=1, contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_future_post_valid_inputs_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/futureethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', deliverydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, commodityname='wheat', price=22, margin=2, soliditycodeinitial='a', transactionid='', spotprice=1, contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertIn('Call Options', response.data)

    def test_future_post_valid_inputs_contract_created(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/futureethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', deliverydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, commodityname='wheat', price=22, margin=2, soliditycodeinitial='samplesoliditycodeishere', transactionid='', spotprice=1, contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertIn('samplesoliditycodeishere', response.data)

    def test_future_post_missing_inputs_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/futureethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', deliverydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, commodityname='wheat', price=22, margin=2, contractfield='', transactionid='', spotprice=1, contractfield2=''), follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_future_post_missing_inputs_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/futureethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', deliverydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, commodityname='wheat', price=22, margin=2, contractfield='', transactionid='', spotprice=1, contractfield2=''), follow_redirects=True)
        self.assertIn("Bad Request", response.data)
        #print response.data

    def test_calloption_post_valid_inputs_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/calloptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='a', contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_calloption_post_valid_inputs_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/calloptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='a', contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertIn('Put Options', response.data)

    def test_calloption_post_valid_inputs_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/calloptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='samplesoliditycodeishere', contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertIn('samplesoliditycodeishere', response.data)

    def test_calloption_post_missing_inputs_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/calloptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='a', contractfield2='a'), follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        # print response.data

    def test_calloption_post_missing_inputs_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/calloptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='a', contractfield2='a'), follow_redirects=True)
        # self.assertIn('Error', response.data)
        # print response.data

    def test_putoption_post_valid_inputs_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='a', contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # print response.data

    def test_putoption_post_valid_inputs_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='a', contractfield2='a', contractfield3='a'), follow_redirects=True)
        #self.assertIn('Call Options', response.data)
        # print response.data

    def test_putoption_post_valid_inputs_contract_created(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='samplesoliditycodeishere', contractfield2='a', contractfield3='a'), follow_redirects=True)
        self.assertIn('samplesoliditycodeishere', response.data)
        # print response.data

    def test_putoption_post_missing_inputs_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='', contractfield2=''), follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        #print response.data
        #probably best to repeat this with a test of what page you wind up on. I think this giving 200 but on error page

    def test_putoption_post_missing_inputs_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='', contractfield2=''), follow_redirects=True)
        #self.assertEqual(response.status_code, 400)
        #print response.data
        #probably best to repeat this with a test of what page you wind up on. I think this giving 200 but on error page


    # def test_putoption_post_missing_inputs_redirect(self):
    #     self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
    #     self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
    #     response = self.app.post('/putoptionethereum', data=dict(buyerethereumaddress='d6aaae06717f25095eab8250369a437e549160a4', sellerethereumaddress='e6aaae06717f25095eab8250369a437e549160a4', expirydateTimestamp=1623492485, blockchainderivativesid='11', numberofunits=22, assetname='wheat', strikeprice=22, premium=2, soliditycodeinitial='', contractfield2=''), follow_redirects=True)
    #     #self.assertEqual(response.status_code, 400)
    #     print response.data
    #     self.assertIn("Error", response.data)

    def test_login_no_existing_user(self):
        response = self.app.post('/login', data=dict(email='username2@email.com', password='password'), follow_redirects=True)
        self.assertIn('NO USER WITH THAT NAME', response.data)

    def test_register_then_login_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_then_login_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.assertIn('To Create and Manage Derivatives Here', response.data)

    def test_register_existing_user_status(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_existing_user_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.assertIn('There is already a user with that name.', response.data)

    def test_register_then_login_then_logout(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_then_login_then_logout_redirect(self):
        self.app.post('/register', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        self.app.post('/login', data=dict(email='username@email.com', password='password'), follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn('To Create and Manage Derivatives Here', response.data)

    def test_logout_without_login_status(self):
        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_without_login_message(self):
        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn('Must be logged-in for that page', response.data)

    def test_logout_without_login_redirect(self):
        self.app.get('/logout', follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn('Enter Your Email', response.data)

if __name__ == '__main__':
    unittest.main()

#run from command line with: python tests.py
