"""
Instabus init
"""

import os, sys

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

sys.path.extend(os.path.dirname(__file__))

# App Setup
app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_object('backend.config.config')

# DB Setup
db = SQLAlchemy(app)

from backend.api import views, models
