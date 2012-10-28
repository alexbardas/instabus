from datetime import datetime
from random import choice
import factory

from api.models import Checkin

class CheckinFactory(factory.Factory):
    FACTORY_FOR = Checkin

    type = choice(['BUS', 'TRA', 'MET'])
    longitude = 26.051791 
    latitude = 44.470611
    line = 'X11'
    created = datetime.now()
