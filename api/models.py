"""
Models
"""

from datetime import datetime

import geoalchemy as geo

from instabus.api.app import db

class Checkin(db.Model):
    """ 
    Model that records when an anonymous user checks in with their location
    """
    __tablename__ = 'checkins'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Unicode, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    location = geo.GeometryColumn(geo.Point(2))

    def __repr__(self):
        return '<Checkin %r>' % (self.id)
