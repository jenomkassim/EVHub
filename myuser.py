from google.appengine.ext import ndb

class MyUser(ndb.Model):
    #email property of user
    email_address = ndb.StringProperty()
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.StringProperty()
    batterysize = ndb.StringProperty
    WLTP_range = ndb.StringProperty
    cost = ndb.StringProperty
    power = ndb.StringProperty