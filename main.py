import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from addcar import AddCar
from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = ''
        login_status = ''

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if user == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.users_id())
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


# starts the application
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addcar', AddCar),
    # ('/displaycars', DisplayCars)
], debug=True)
