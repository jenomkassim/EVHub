from google.appengine.ext import ndb

class MyUser(ndb.Model):
    #email property of user
    email_address = ndb.StringProperty()