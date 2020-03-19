import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

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
        error_message = ''
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
            'car_deets': car_deets,
            'idd': idd,
            'error_message': error_message
        }

        template = JINJA_ENVIRONMENT.get_template('car-details.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        error_message = ''
        success_message = ''
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        action = self.request.get('button')
        idd = self.request.get('id')
        error_message = ''

        idd = self.request.get('id')
        hi = ndb.Key(urlsafe=idd)
        car_id = hi.id()

        car_deets = ndb.Key('Vehicles', car_id).get()

        if action == 'Submit':
            car_deets.name = self.request.get('vehicle_name')
            car_deets.manufacturer = self.request.get('vehicle_manufacturer')
            car_deets.year = int(self.request.get('vehicle_year'))
            car_deets.batterySize = float(self.request.get('vehicle_batterySize'))
            car_deets.WLTP_range = int(self.request.get('vehicle_WLTP_range'))
            car_deets.cost = int(self.request.get('vehicle_cost'))
            car_deets.power = int(self.request.get('vehicle_power'))

            car_query = Vehicles.query()
            query = car_query.filter(Vehicles.name == car_deets.name, Vehicles.manufacturer == car_deets.manufacturer,
                                     Vehicles.year == car_deets.year).fetch()

            if len(query) == 0:
                car_deets.put()
                success_message = 'Car Successfully Updated'
            else:
                error_message = 'Car Exists In The Database'

        if action == 'Yes':
            car_deets.key.delete()
            self.redirect('/search-cars')

        # self.response.write('Name = ' + car_deets.name)
        # self.response.write('<br/>Manufacturer = ' + car_deets.manufacturer)
        # self.response.write('<br/>Year = ' + str(car_deets.year))
        # self.response.write('<br/>Battery = ' + str(car_deets.batterySize))
        # self.response.write('<br/>Range = ' + str(car_deets.WLTP_range))
        # self.response.write('<br/>Cost = ' + str(car_deets.cost))
        # self.response.write('<br/>Power = ' + str(car_deets.power))

        # self.redirect('/car-details?id=' + str(idd))
        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'car_deets': car_deets,
            'idd': idd,
            'error_message': error_message,
            'success_message': success_message
        }

        template = JINJA_ENVIRONMENT.get_template('car-details.html')
        self.response.write(template.render(template_values))
