from google.appengine.ext import ndb

from review import ReviewAndRating


class Vehicles(ndb.Model):
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    batterySize = ndb.FloatProperty()
    WLTP_range = ndb.IntegerProperty()
    cost = ndb.IntegerProperty()
    power = ndb.IntegerProperty()
    review = ndb.StructuredProperty(ReviewAndRating, repeated=True)
