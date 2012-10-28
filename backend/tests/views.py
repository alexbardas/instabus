"""
views.py tests
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import flask
from flask import json

import api
from tests.factories import CheckinFactory

class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.app

    def tearDown(self):
        pass
    
    def test_checkin_GET(self):
        response = self.app.test_client().get('/api/checkin')
        assert 'checkin' in response.data
    
    def test_checkin_POST(self):
        response = self.app.test_client().post('/api/checkin',
            data=CheckinFactory.attributes())
        data = json.loads(response.data)
        assert data['status'] == "OK"
        assert data['message'] == "Checked in!"
    
    def test_realtime_GET(self):
        with self.app.test_request_context('/api/realtime',
            method='GET'):
            pass

    def test_realtime_DELETE(self):
        response = self.app.test_client().delete('/api/realtime')
        data = json.loads(response.data)
        assert data['status'] == "OK"
        assert data['message'] == "Checked out!"

if __name__ == '__main__':
    unittest.main()
