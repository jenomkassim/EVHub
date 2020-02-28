from google.appengine.ext import ndb


class Vehicles(ndb.Model):
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    batterySize = ndb.FloatProperty()
    WLTP_range = ndb.IntegerProperty()
    cost = ndb.IntegerProperty()
    power = ndb.IntegerProperty()
