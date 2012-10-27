"""
Models
"""

from instabus.app import db

class Checkin(db.Model):
    """ 
    Model that records when an anonymous user checks in with their location
    """
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Checkin %r>' % (self.id)
