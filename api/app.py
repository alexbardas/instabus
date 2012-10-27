"""
Instabus
"""

import os

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from models import Checkin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

@app.route('/api/checkin', methods=['GET', 'POST'])
def checkin():
    """ 
    POST: Create a new Checkin
    GET:  Return all Checkins
    """
    if request.method == 'POST':
      # Create the model
      return 'Checked in!'
    else:
      checkins = Checkin.query.all()
      return checkins

@app.route('/api/checkin/<checkin_id>', methods=['GET'])
def checkin(checkin_id):
    """ 
    Fetch the Checkin model with the given id
    """
    checkin = Checkin.query.get(checkin_id)
    return jsonify(type=checkin.type,
                   created=checkin.created,
                   longitude=checkin.longitude,
                   latitude=checkin.latitude)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
