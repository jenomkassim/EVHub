from google.appengine.ext import ndb


class ReviewAndRating(ndb.Model):
    review = ndb.StringProperty()
    rating = ndb.IntegerProperty()
