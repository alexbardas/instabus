"""
Models
"""

from datetime import datetime

from backend.api import db

class DataPoint(db.Model):
    """ Model a datapoint received from a user's mobile. """
    __tablename__ = 'datapoints'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Unicode, nullable=False, index=True)
    line = db.Column(db.Unicode, nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, nullable=False, index=True)
    is_demo = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Integer, nullable=False, index=True)
    session = db.Column(db.Unicode, nullable=False, index=True)


class Checkin(db.Model):
    """ 
    Model that records when an anonymous user checks in with their location
    """
    __tablename__ = 'checkins'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Unicode, nullable=False)
    line = db.Column(db.Unicode, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):
        return '<Checkin %r>' % (self.id)
