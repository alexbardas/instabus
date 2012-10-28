"""
Instabus Views
"""
# pylint: disable=W0312

from time import time
import uuid

from flask import request, jsonify, session, json, Response
from functools import wraps
from redis import Redis

from backend.api import app, db
from backend.api.models import Checkin, DataPoint


redis = Redis()

def save_datapoint(request):
	get_post_field = lambda x: request.form[x]
	if not session.has_key('id'):
		session['id'] = int(uuid.uuid4())

	data_point_post_data = {
		'type': get_post_field('type'),
		'line': get_post_field('line'),
		'latitude': get_post_field('latitude'),
		'longitude': get_post_field('longitude'),
		'created': get_post_field('created'), # Convert to datetime.
		'is_demo': int(get_post_field('is_demo')),
		'is_active': int(get_post_field('is_active')),
		'session': session['id'],
	}

	db.session.add(DataPoint(**data_point_post_data))
	db.session.commit()


@app.route('/api/datapoint', methods=['POST'])
def save_datapoint():
	""" Save and return data about datapoints."""
	save_datapoint(request)

	return jsonify(status='OK', message='Saved datapoint {0}, {1}.'.format(
		get_post_field('latitude'), get_post_field('longitude')))

@app.route('/ms')
def ms():
	return Response('')

@app.route('/api/datapoint/<line_no>')
def get_datapoint(line_no):
	# pylint: disable=E1101
	"""
	datapoints = DataPoint.query\
			.filter_by(line=line_no)\
			.filter_by(is_active=1)\
			.all()
	print(datapoints)
	"""
	return jsonify(status='OK')

def sessionify(func):
    @wraps(func)
    def wrapped():
        if not session.has_key('id'):
            session['id'] = int(uuid.uuid4())
        return func()
    return wrapped

@app.route('/api/checkin', methods=['GET', 'POST'])
@sessionify
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
        checkins = Checkin.query.all()
        checkins = [{ 
                      'id': checkin.id,
                      'type': checkin.type,
                      'longitude': checkin.longitude,
                      'latitude': checkin.latitude,
                      'line': checkin.line,
                      'created': checkin.created.strftime("%Y-%m-%d %H:%M"),
                    } for checkin in checkins]
        return Response(response=json.dumps(checkins), 
            mimetype='application/json')

@app.route('/api/realtime', methods=['GET', 'POST', 'DELETE'])
@sessionify
def realtime():
	"""
	Handle realtime data coming in from online users
	POST: Insert data into redis (use session id to track individual users)
	GET: Return current realtime data
	DELETE: Explicit checkout, delete the users realtime updates
	"""
	# Get the current session id.
	session_id = None if 'id' not in session else session['id']

	# If we have a POST request, we save the data point.
	if request.method == 'POST':
		try:
			save_datapoint(request) 
			return jsonify(status="OK", message="Position updated")
		except KeyError, e:
			return jsonify(status="ERROR", message="Problem updating position")
	# When a DELETE request is received, we delete all datapoints with a
	# given session_id.
	elif request.method == 'DELETE':
		if session_id:
			# Mark a certain session as being inactive.
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
			records = [record for record in records 
												if record['type'] == vehicle_type]
			return Response(response=json.dumps(records), 
					mimetype='application/json')
