from google.appengine.ext import ndb


class MyUser(ndb.Model):
    #email property of user
    username = ndb.StringProperty()
