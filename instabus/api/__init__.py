"""
Instabus init
"""

import os, sys

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

sys.path.extend(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
app.config.from_object('api.config')
db = SQLAlchemy(app)

from api import views, models
