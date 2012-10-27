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
        try:
            attributes = {
                'type': request.form['type'],
                'longitude': request.form['longitude'],
                'latitude': request.form['latitude'],
            }

            checkin = Checkin(**attributes)
            # Needs to be committed
            attributes['id'] = checkin.id

            return jsonify(**attributes)
        except Exception, e:
            return jsonify(error="ERROR: %s" % e)
    else:
        checkin = Checkin.query.first()
        return jsonify(id=checkin.id, type=checkin.type)
