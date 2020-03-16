import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class CarDetails(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        # idd = int(self.request.get('id'))
        idd = self.request.get('id')
        hi = ndb.Key(urlsafe=idd)
        car_id = hi.id()

        car_deets = ndb.Key('Vehicles', car_id).get()

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'car_deets': car_deets
        }

        template = JINJA_ENVIRONMENT.get_template('car-details.html')
        self.response.write(template.render(template_values))
