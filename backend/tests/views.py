"""
views.py tests
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import tempfile
import unittest

import api

from tests.factories import CheckinFactory

class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        api.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        self.app = api.app.test_client()

    def tearDown(self):
        pass
    
    def test_checkin_GET(self):
        response = self.app.get('/api/checkin/')
        assert 'test' in response.data
    
    def test_checkin_POST(self):
        response = self.app.post('/api/checkin/')
        assert 'something' == 'somethingelse'

if __name__ == '__main__':
    unittest.main()
