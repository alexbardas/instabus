"""
views.py tests
"""

import os
from redis import Redis; redis = Redis()
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import flask
from flask import json

import api
from api.models import Checkin
from tests.factories import CheckinFactory

class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.app

    def tearDown(self):
        pass
    
    def test_checkin_GET(self):
        response = self.app.test_client().get('/api/checkin')
        data = json.loads(response.data)
        assert len(data) == len(Checkin.query.all())
    
    def test_checkin_POST(self):
        response = self.app.test_client().post('/api/checkin',
            data=CheckinFactory.attributes())
        data = json.loads(response.data)
        assert data['status'] == "OK"
        assert data['message'] == "Checked in!"
    
    def test_realtime_GET(self):
        response = self.app.test_client().get('/api/realtime')
        data = json.loads(response.data)
        assert (data[0].has_key('is_demo') and
                data[0].has_key('created') and
                data[0].has_key('line') and
                data[0].has_key('longitude') and
                data[0].has_key('latitude') and
                data[0].has_key('type'))
        assert len(data) == len(redis.keys())

    def test_realtime_DELETE(self):
        response = self.app.test_client().delete('/api/realtime')
        data = json.loads(response.data)
        assert data['status'] == "OK"
        assert data['message'] == "Checked out!"

if __name__ == '__main__':
    unittest.main()
