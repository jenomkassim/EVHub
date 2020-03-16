import os

import jinja2
import webapp2
from google.appengine.api import users

from vehicles import Vehicles

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

        idd = int(self.request.get('id'))
        car_deets = Vehicles.get_by_id(idd)

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'car_deets': car_deets
        }

        template = JINJA_ENVIRONMENT.get_template('car-details.html')
        self.response.write(template.render(template_values))
