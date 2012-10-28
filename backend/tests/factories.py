import os
from datetime import datetime
from random import choice

import factory
from flask import json

from api.models import Checkin

data_points = json.load(open(os.path\
    .join(os.path.dirname(__file__), '../data/300.json')))

class CheckinFactory(factory.Factory):
    FACTORY_FOR = Checkin

    type = choice(['BUS', 'TRA', 'MET'])
    longitude = choice(data_points)[0] 
    latitude = choice(data_points)[1] 
    line = choice(['X11', 'C54', 'B21'])
    created = datetime.now()
