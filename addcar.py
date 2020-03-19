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


class AddCar(webapp2.RequestHandler):
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

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status
        }

        template = JINJA_ENVIRONMENT.get_template('addcar.html')
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

        if self.request.get('add-car-button') == 'Submit':

            newCar = Vehicles()

            newCar.name = self.request.get('vehicle_name')
            newCar.manufacturer = self.request.get('vehicle_manufacturer')
            newCar.year = int(self.request.get('vehicle_year'))
            newCar.batterySize = float(self.request.get('vehicle_batterySize'))
            newCar.WLTP_range = int(self.request.get('vehicle_WLTP_range'))
            newCar.cost = int(self.request.get('vehicle_cost'))
            newCar.power = int(self.request.get('vehicle_power'))

            car_query = Vehicles.query()
            query = car_query.filter(Vehicles.name == newCar.name, Vehicles.manufacturer == newCar.manufacturer,
                                     Vehicles.year == newCar.year).fetch()

            if len(query) == 0:
                newCar.put()
                success_message = 'Car Successfully Added To The Database'
                # self.redirect('/addcar')
            else:
                error_message = 'Car Exists In The Database'
                # self.response.write('Car Exists In The Database')
                # self.redirect('/addcar')

            #
            # success_message = "Car Added To The Database Successfully"
            #


        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'vehicle_name': newCar.name,
            'vehicle_manufacturer': newCar.manufacturer,
            'vehicle_year': newCar.year,
            'vehicle_batterySize': newCar.batterySize,
            'vehicle_WLTP_range': newCar.WLTP_range,
            'vehicle_cost': newCar.cost,
            'vehicle_power': newCar.power,
            'error_message': error_message,
            'success_message': success_message
        }

        template = JINJA_ENVIRONMENT.get_template('addcar.html')
        self.response.write(template.render(template_values))



