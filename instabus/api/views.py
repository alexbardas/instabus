"""
Instabus Views
"""

from flask import request, jsonify, session
from redis import Redis
redis = Redis(host='localhost', db=0)

from api import app, db
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
            db.session.add(checkin)
            db.session.commit()

            attributes['id'] = checkin.id

            return jsonify(**attributes)
        except Exception, e:
            return jsonify({'status': 'ERROR', 'message': '3 params are needed: type, longitutde, latitude'})
    else:
        redis.set('test', 'test')
        checkin = Checkin.query.first()
        return jsonify(id=checkin.id, type=checkin.type)

@app.route('/api/realtime', methods=['GET', 'POST', 'DELETE'])
def realtime():
    """
    Handle realtime data coming in from online users
    POST: Insert data into redis (use session id to track individual users)
    GET: Return current realtime data
    DELETE: Explicit checkout, delete the users realtime updates
    """
    if request.method == 'POST':
        try:
            type = request.form['type']
            longitude = request.form['longitude']
            latitude = request.form['latitude']
            return 'post'
        except KeyError, e:
            return 'error'
    elif request.method == 'DELETE':
        return 'delete'
    else:
        type = request.args.get('type', 'all')
        # Return all realtime data
        if type == 'all':
            response = redis.get('test')
            redis.set('test', None)
            return response
        # Return the data filtered by the transport type
        else:
            redis.set(type, 'blah')
            response = redis.get(type)
            response = str(session['id'])
            return response
