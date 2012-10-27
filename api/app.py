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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
