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
        type = request.form['type']
        longitude = request.form['longitude']
        latitude = request.form['latitude']

        checkin = Checkin(type=type, longitude=longitude, 
            latitude=latitude)
        # Needs to be committed
        response = {
            'id': checkin.id,
            'type': checkin.type, 
            'longitude': checkin.longitude,
            'latitude': checkin.latitude,
        }

        return jsonify(**response)
    else:
        checkin = Checkin.query.first()

        response = {
            'id': checkin.id,
            'type': checkin.type, 
            'longitude': checkin.longitude,
            'latitude': checkin.latitude,
        }

        return jsonify(**response)
