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


class SearchCars(webapp2.RequestHandler):
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

        total_query = Vehicles.query()

        count = 0

        for i in total_query:
            count = count + 1

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'total_query': total_query,
            'count': count
        }

        template = JINJA_ENVIRONMENT.get_template('search-cars.html')
        self.response.write(template.render(template_values))

    def post(self):
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

        action = self.request.get('Search')
        count = 0

        if action == 'Search':
            name = self.request.get('vehicleName')
            manufacturer = self.request.get('manufacturer')
            lower_year = self.request.get('lower_year')
            upper_year = self.request.get('upper_year')
            battery_lower = self.request.get('battery_lower')
            battery_upper = self.request.get('battery_upper')
            range_lower = self.request.get('range_lower')
            range_upper = self.request.get('range_upper')
            cost_lower = self.request.get('cost-lower')
            cost_upper = self.request.get('cost-upper')
            power_lower = self.request.get('power-lower')
            power_upper = self.request.get('power-upper')

        # Values if empty
        if len(lower_year) == 0:
            lower_year = int(2010)
        if len(upper_year) == 0:
            upper_year = int(2022)
        if len(battery_lower) == 0:
            battery_lower = float(50)
        if len(battery_upper) == 0:
            battery_upper = float(550)
        if len(range_lower) == 0:
            range_lower = 200
        if len(range_upper) == 0:
            range_upper = 850
        if len(cost_lower) == 0:
            cost_lower = int(20000)
        if len(cost_upper) == 0:
            cost_upper = int(80000)
        if len(power_lower) == 0:
            power_lower = int(50)
        if len(power_upper) == 0:
            power_upper = int(300)

        # Year Comparison
        if int(lower_year) >= 2010 and int(lower_year) <= 2022:
            year_lower_error_message = ''
            year_lower_error_style = ''
        else:
            year_lower_error_message = 'Year is below 2010 or above 2022'
            year_lower_error_style = 'error_style'

        if int(upper_year) >= 2010 and int(upper_year) <= 2022:
            year_higher_error_message = ''
            year_higher_error_style = ''
        else:
            year_higher_error_message = 'Year is below 2010 or above 2022'
            year_higher_error_style = 'error_style'

        # Battery Comparison
        if float(battery_lower) >= 50.0 and float(battery_lower) <= 550.0:
            battery_lower_error_message = ''
            battery_lower_error_style = ''
        else:
            battery_lower_error_message = 'Battery size is below 50.0Kwh or above 550.0Kwh'
            battery_lower_error_style = 'error_style'

        if float(battery_upper) >= 50.0 and float(battery_upper) <= 550.0:
            battery_higher_error_message = ''
            battery_higher_error_style = ''
        else:
            battery_higher_error_message = 'Battery size is below 50.0Kwh or above 550.0Kwh'
            battery_higher_error_style = 'error_style'

        # Range Comparison
        if int(range_lower) >= 200 and int(range_lower) <= 850:
            range_lower_error_message = ''
            range_lower_error_style = ''
        else:
            range_lower_error_message = 'Range is below 200km or above 850km'
            range_lower_error_style = 'error_style'

        if int(range_upper) >= 200 and int(range_upper) <= 850:
            range_higher_error_message = ''
            range_higher_error_style = ''
        else:
            range_higher_error_message = 'Range is below 200km or above 850km'
            range_higher_error_style = 'error_style'

        # Cost Comparison
        if int(cost_lower) >= 20000 and int(cost_lower) <= 80000:
            cost_lower_error_message = ''
            cost_lower_error_style = ''
        else:
            cost_lower_error_message = 'Cost is below 20,000 or above 80,000'
            cost_lower_error_style = 'error_style'

        if int(cost_upper) >= 20000 and int(cost_upper) <= 80000:
            cost_higher_error_message = ''
            cost_higher_error_style = ''
        else:
            cost_higher_error_message = 'Cost is below 20,000 or above 80,000'
            cost_higher_error_style = 'error_style'

        # Power Comparison
        if int(power_lower) >= 50 and int(power_lower) <= 300:
            power_lower_error_message = ''
            power_lower_error_style = ''
        else:
            power_lower_error_message = 'Power is below 50kW or above 300kW'
            power_lower_error_style = 'error_style'

        if int(power_upper) >= 50 and int(power_upper) <= 300:
            power_upper_error_message = ''
            power_upper_error_style = ''
        else:
            power_upper_error_message = 'Power is below 50kW or above 300kW'
            power_upper_error_style = 'error_style'

        # manufacturer = str(manufacturer)
        lower_year = int(lower_year)
        upper_year = int(upper_year)
        battery_lower = float(battery_lower)
        battery_upper = float(battery_upper)
        range_lower = int(range_lower)
        range_upper = int(range_upper)
        cost_lower = int(cost_lower)
        cost_upper = int(cost_upper)
        power_lower = int(power_lower)
        power_upper = int(power_upper)

        car_query = Vehicles.query()

        year_query = car_query.filter(Vehicles.year >= lower_year, Vehicles.year <= upper_year).fetch(keys_only=True)
        battery_query = car_query.filter(Vehicles.batterySize >= battery_lower,
                                         Vehicles.batterySize <= battery_upper).fetch(keys_only=True)
        range_query = car_query.filter(Vehicles.WLTP_range >= range_lower, Vehicles.WLTP_range <= range_upper).fetch(
            keys_only=True)
        cost_query = car_query.filter(Vehicles.cost >= cost_lower, Vehicles.cost <= cost_upper).fetch(keys_only=True)
        power_query = car_query.filter(Vehicles.power >= power_lower, Vehicles.power <= power_upper) \
            .fetch(keys_only=True)

        if len(name) == 0 and len(manufacturer) == 0:
            total_query = ndb.get_multi(set(year_query).intersection(battery_query).intersection(range_query)
                                        .intersection(cost_query).intersection(power_query))
            for i in total_query:
                count = count + 1

        elif len(name) == 0:
            manufacturer_query = Vehicles.query(Vehicles.manufacturer == manufacturer).fetch(keys_only=True)
            total_query = ndb.get_multi(set(manufacturer_query).intersection(year_query).intersection(battery_query)
                                        .intersection(range_query).intersection(cost_query).intersection(power_query))

            for i in total_query:
                count = count + 1

        elif len(manufacturer) == 0:
            name_query = Vehicles.query(Vehicles.name == name).fetch(keys_only=True)
            total_query = ndb.get_multi(set(name_query).intersection(year_query).intersection(battery_query)
                                        .intersection(range_query).intersection(cost_query).intersection(power_query))

            for i in total_query:
                count = count + 1
        else:
            name_query = Vehicles.query(Vehicles.name == name).fetch(keys_only=True)
            manufacturer_query = Vehicles.query(Vehicles.manufacturer == manufacturer).fetch(keys_only=True)
            total_query = ndb.get_multi(set(name_query).intersection(manufacturer_query).intersection(year_query)
                                        .intersection(battery_query).intersection(range_query).intersection(cost_query)
                                        .intersection(power_query))

            for i in total_query:
                count = count + 1

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,

            'name': name,
            'manufacturer': manufacturer,
            'lower_year': lower_year,
            'upper_year': upper_year,
            'battery_lower': battery_lower,
            'battery_upper': battery_upper,
            'range_lower': range_lower,
            'range_upper': range_upper,

            'year_lower_error_message': year_lower_error_message,
            'year_lower_error_style': year_lower_error_style,
            'year_higher_error_message': year_higher_error_message,
            'year_higher_error_style': year_higher_error_style,

            'battery_lower_error_message': battery_lower_error_message,
            'battery_lower_error_style': battery_lower_error_style,
            'battery_higher_error_message': battery_higher_error_message,
            'battery_higher_error_style': battery_higher_error_style,

            'range_lower_error_message': range_lower_error_message,
            'range_lower_error_style': range_lower_error_style,
            'range_higher_error_message': range_higher_error_message,
            'range_higher_error_style': range_higher_error_style,

            'cost_lower_error_message': cost_lower_error_message,
            'cost_lower_error_style': cost_lower_error_style,
            'cost_higher_error_message': cost_higher_error_message,
            'cost_higher_error_style': cost_higher_error_style,

            'power_lower_error_message': power_lower_error_message,
            'power_lower_error_style': power_lower_error_style,
            'power_upper_error_message': power_upper_error_message,
            'power_upper_error_style': power_upper_error_style,

            'year_query': year_query,
            'battery_query': battery_query,
            'range_query': range_query,
            'cost_query': cost_query,
            'power_query': power_query,
            'total_query': total_query,
            'count': count
            # 'success_message': success_message
        }

        template = JINJA_ENVIRONMENT.get_template('search-cars.html')
        self.response.write(template.render(template_values))

        # query = car_query.filter(Vehicles.name == name, Vehicles.manufacturer == manufacturer,
        #                               Vehicles.year == year).fetch()
