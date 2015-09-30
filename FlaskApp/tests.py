import os
import app 
#from app import app
import app
import unittest 
from unittest import TestCase
import tempfile
#from flask import Flask
#from flask.ext.testing import TestCase

class AppTestCase(unittest.TestCase):

    def setUp(self):
        #app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('username', 'password')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

if __name__ == '__main__':
    unittest.main()

#run from command line with: python tests.py
