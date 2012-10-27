"""
Instabus Views
"""

from flask import request, jsonify, json

from api import app
from api.models import Checkin

@app.route('/api/checkin', methods=['GET', 'POST'])
def checkin():
    """ 
    POST: Create a new Checkin
    GET:  Return all Checkins
    """
    if request.method == 'POST':
        checkin = Checkin
        return 'Checked in!'
    else:
        checkins = Checkin.query.all()
        print checkins
        return json.dumps(checkins)
