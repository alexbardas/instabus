"""
Instabus Views
"""

from flask import request, jsonify, session, json, Response
from redis import Redis
redis = Redis()
from time import time

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
                'line': request.form['line'],
            }

            checkin = Checkin(**attributes)
            db.session.add(checkin)
            db.session.commit()

            attributes['id'] = checkin.id

            return jsonify(status="OK", message="Checked in!")
        except Exception, e:
            return jsonify(status='ERROR', 
                message='3 params are needed: type, longitude, latitude')
    else:
        return 'checkin'

@app.route('/api/realtime', methods=['GET', 'POST', 'DELETE'])
def realtime():
    """
    Handle realtime data coming in from online users
    POST: Insert data into redis (use session id to track individual users)
    GET: Return current realtime data
    DELETE: Explicit checkout, delete the users realtime updates
    """
    session_id = str(session['id'])
    if request.method == 'POST':
        try:
            attributes = {
                'type': request.form['type'],
                'longitude': request.form['longitude'],
                'latitude': request.form['latitude'],
                'line': request.form['line'],
                'created': int(time.now()),
                'is_demo': request.form['is_demo'],
            }
            redis.set(session_id, attributes)
            return jsonify(status="OK", message="Position updated")
        except KeyError, e:
            return jsonify(status="ERROR", message="Problem updating position")
    elif request.method == 'DELETE':
        redis.delete(session_id)
        return jsonify(status="OK", message="Checked out!")
    else:
        vehicle_type = request.args.get('type', 'all')
        # Return all realtime data
        if vehicle_type == 'all':
            keys = redis.keys()
            records = []
            for key in keys:
                records.append(redis.get(key))
            return Response(response=json.dumps(records), 
                mimetype='application/json')
        # Return the data filtered by the transport type
        else:
            keys = redis.keys()
            records = []
            for key in keys:
                records.append(redis.get(key))
            # Redis isn't the best choice for queries
            # Could be refactored to use e.g. postgres or mongodb
            records = [record for record 
                              in records 
                              if record['type'] == vehicle_type]
            return Response(response=json.dumps(records), 
                mimetype='application/json')
