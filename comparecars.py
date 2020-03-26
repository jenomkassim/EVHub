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


class CompareCars(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        error_message = ''
        user = users.get_current_user()
        hasSearched = False

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'hasSearched': hasSearched,
            'error_message': error_message
        }

        template = JINJA_ENVIRONMENT.get_template('comparecar.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        error_message = ''
        success_message = ''
        user = users.get_current_user()
        yearStyle1 = ''
        yearStyle2 = ''
        yearStyle3 = ''
        yearStyle4 = ''
        yearCost1 = ''
        yearCost2 = ''
        yearCost3 = ''
        yearCost4 = ''
        BatteryStyle1 = ''
        BatteryStyle2 = ''
        BatteryStyle3 = ''
        BatteryStyle4 = ''
        RangeStyle1 = ''
        RangeStyle2 = ''
        RangeStyle3 = ''
        RangeStyle4 = ''
        PowerStyle1 = ''
        PowerStyle2 = ''
        PowerStyle3 = ''
        PowerStyle4 = ''
        hasSearched = True
        v1Link = True
        v2Link = True
        v3Link = True
        v4Link = True

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        action = self.request.get('compare-car-button')

        class VehicleResult(object):
            name = "N/A"
            manufacturer = "N/A"
            year = "N/A"
            cost = "N/A"
            batterySize = "N/A"
            WLTP_range = "N/A"
            power = "N/A"

        class VehicleResultValues(object):
            name = "N/A"
            manufacturer = "N/A"
            year = 0
            cost = 0
            batterySize = 0
            WLTP_range = 0
            power = 0

        if action == 'Compare':
            vehicle_1 = self.request.get('vehicle_1')
            vehicle_1_year = self.request.get('vehicle_1_year')
            vehicle_2 = self.request.get('vehicle_2')
            vehicle_2_year = self.request.get('vehicle_2_year')
            vehicle_3 = self.request.get('vehicle_3')
            vehicle_3_year = self.request.get('vehicle_3_year')
            vehicle_4 = self.request.get('vehicle_4')
            vehicle_4_year = self.request.get('vehicle_4_year')

        # self.response.write('V1 = ' + vehicle_1)
        # self.response.write('<br/>V1 Year = ' + str(vehicle_1_year))
        # self.response.write('<br/>V2 = ' + vehicle_2)
        # self.response.write('<br/>V2 Year = ' + str(vehicle_2_year))
        # self.response.write('<br/>V3 = ' + vehicle_3)
        # self.response.write('<br/>V3 Year = ' + vehicle_3_year)
        # self.response.write('<br/>V4 = ' + vehicle_4)
        # self.response.write('<br/>V4 Year = ' + str(vehicle_4_year))

        car_query = Vehicles.query()
        vehicle_1_query = Vehicles.query(Vehicles.name == vehicle_1).fetch(keys_only=True)
        vehicle_1_year_query = car_query.filter(Vehicles.year == int(vehicle_1_year)).fetch(keys_only=True)
        v1_total_query = ndb.get_multi(set(vehicle_1_query).intersection(vehicle_1_year_query))

        vehicle_2_query = Vehicles.query(Vehicles.name == vehicle_2).fetch(keys_only=True)
        vehicle_2_year_query = car_query.filter(Vehicles.year == int(vehicle_2_year)).fetch(keys_only=True)
        v2_total_query = ndb.get_multi(set(vehicle_2_query).intersection(vehicle_2_year_query))

        vehicle_3_query = Vehicles.query(Vehicles.name == vehicle_3).fetch(keys_only=True)
        vehicle_3_year_query = car_query.filter(Vehicles.year == int(vehicle_3_year)).fetch(keys_only=True)
        v3_total_query = ndb.get_multi(set(vehicle_3_query).intersection(vehicle_3_year_query))

        vehicle_4_query = Vehicles.query(Vehicles.name == vehicle_4).fetch(keys_only=True)
        vehicle_4_year_query = car_query.filter(Vehicles.year == int(vehicle_4_year)).fetch(keys_only=True)
        v4_total_query = ndb.get_multi(set(vehicle_4_query).intersection(vehicle_4_year_query))

        for i in v1_total_query:
            v1 = i

        for i in v2_total_query:
            v2 = i

        for i in v3_total_query:
            v3 = i

        for i in v4_total_query:
            v4 = i

        # CALCULATE IF NO INPUT IN VEHICLE 3 AND 4
        if vehicle_3 == "" and vehicle_4 == "":

            vrv = VehicleResultValues()
            vr = VehicleResult()
            v3 = vr
            v4 = vr
            v3Link = False
            v4Link = False

            if len(v1_total_query) != 1:
                v1 = vrv
                v1Link = False

            if len(v2_total_query) != 1:
                v2 = vrv
                v2Link = False

            # YEAR MIN AND MAX
            my_list = [v1.year, v2.year]
            max_value = max(my_list)
            max_index = my_list.index(max_value)
            min_value = min(i for i in my_list if i > 0)
            min_index = my_list.index(min_value)

            # COST MIN AND MAX
            my_cost_list = [v1.cost, v2.cost]
            max_cost_value = max(my_cost_list)
            max_cost_index = my_cost_list.index(max_cost_value)
            min_cost_value = min(i for i in my_cost_list if i > 0)
            min_cost_index = my_cost_list.index(min_cost_value)

            # BATTERY SIZE MIN AND MAX
            my_battery_list = [v1.batterySize, v2.batterySize]
            max_battery_value = max(my_battery_list)
            max_battery_index = my_battery_list.index(max_battery_value)
            min_battery_value = min(i for i in my_battery_list if i > 0)
            min_battery_index = my_battery_list.index(min_battery_value)

            # WLTP RANGE MIN AND MAX
            my_range_list = [v1.WLTP_range, v2.WLTP_range]
            max_range_value = max(my_range_list)
            max_range_index = my_range_list.index(max_range_value)
            min_range_value = min(i for i in my_range_list if i > 0)
            min_range_index = my_range_list.index(min_range_value)

            # POWER MIN AND MAX
            my_power_list = [v1.power, v2.power]
            max_power_value = max(my_power_list)
            max_power_index = my_power_list.index(max_power_value)
            min_power_value = min(i for i in my_power_list if i > 0)
            min_power_index = my_power_list.index(min_power_value)

            self.response.write('</br>Max Index = ' + str(max_power_index))
            self.response.write('</br>Max Power = ' + str(max_power_value))
            self.response.write('</br>Min Index = ' + str(min_power_index))
            self.response.write('</br>Min Power = ' + str(min_power_value))

            # YEAR LOGIC FOR STYLING
            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
            elif max_index == 0:
                yearStyle1 = 'text-success font-weight-bold'
            elif max_index == 1:
                yearStyle2 = 'text-success font-weight-bold'
            elif max_index == 2:
                yearStyle3 = 'text-success font-weight-bold'
            elif max_index == 3:
                yearStyle4 = 'text-success font-weight-bold'

            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
            elif min_index == 0:
                yearStyle1 = 'text-danger font-weight-bold'
            elif min_index == 1:
                yearStyle2 = 'text-danger font-weight-bold'
            elif min_index == 2:
                yearStyle3 = 'text-danger font-weight-bold'
            elif min_index == 3:
                yearStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearStyle2 = ''

            # COST LOGIC FOR STYLING
            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
            elif max_cost_index == 0:
                yearCost1 = 'text-danger font-weight-bold'
            elif max_cost_index == 1:
                yearCost2 = 'text-danger font-weight-bold'
            elif max_cost_index == 2:
                yearCost3 = 'text-danger font-weight-bold'
            elif max_cost_index == 3:
                yearCost4 = 'text-danger font-weight-bold'

            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
            elif min_cost_index == 0:
                yearCost1 = 'text-success font-weight-bold'
            elif min_cost_index == 1:
                yearCost2 = 'text-success font-weight-bold'
            elif min_cost_index == 2:
                yearCost3 = 'text-success font-weight-bold'
            elif min_cost_index == 3:
                yearCost4 = 'text-success font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearCost1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearCost2 = ''

            # BATTERY LOGIC FOR STYLING
            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
            elif max_battery_index == 0:
                BatteryStyle1 = 'text-success font-weight-bold'
            elif max_battery_index == 1:
                BatteryStyle2 = 'text-success font-weight-bold'
            elif max_battery_index == 2:
                BatteryStyle3 = 'text-success font-weight-bold'
            elif max_battery_index == 3:
                BatteryStyle4 = 'text-success font-weight-bold'

            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
            elif min_battery_index == 0:
                BatteryStyle1 = 'text-danger font-weight-bold'
            elif min_battery_index == 1:
                BatteryStyle2 = 'text-danger font-weight-bold'
            elif min_battery_index == 2:
                BatteryStyle3 = 'text-danger font-weight-bold'
            elif min_battery_index == 3:
                BatteryStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                BatteryStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                BatteryStyle2 = ''

            # WLTP RANGE FOR STYLING
            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
            elif max_range_index == 0:
                RangeStyle1 = 'text-success font-weight-bold'
            elif max_range_index == 1:
                RangeStyle2 = 'text-success font-weight-bold'
            elif max_range_index == 2:
                RangeStyle3 = 'text-success font-weight-bold'
            elif max_range_index == 3:
                RangeStyle4 = 'text-success font-weight-bold'

            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
            elif min_range_index == 0:
                RangeStyle1 = 'text-danger font-weight-bold'
            elif min_range_index == 1:
                RangeStyle2 = 'text-danger font-weight-bold'
            elif min_range_index == 2:
                RangeStyle3 = 'text-danger font-weight-bold'
            elif min_range_index == 3:
                RangeStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                RangeStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                RangeStyle2 = ''

            # POWER FOR STYLING
            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
            elif max_power_index == 0:
                PowerStyle1 = 'text-success font-weight-bold'
            elif max_power_index == 1:
                PowerStyle2 = 'text-success font-weight-bold'
            elif max_power_index == 2:
                PowerStyle3 = 'text-success font-weight-bold'
            elif max_power_index == 3:
                PowerStyle4 = 'text-success font-weight-bold'

            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
            elif min_power_index == 0:
                PowerStyle1 = 'text-danger font-weight-bold'
            elif min_power_index == 1:
                PowerStyle2 = 'text-danger font-weight-bold'
            elif min_power_index == 2:
                PowerStyle3 = 'text-danger font-weight-bold'
            elif min_power_index == 3:
                PowerStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                PowerStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                PowerStyle2 = ''

            template_values = {
                'user': user,
                'url': url,
                'login_status': login_status,
                'v1': v1,
                'v2': v2,
                'v3': v3,
                'v4': v4,
                'yearStyle1': yearStyle1,
                'yearStyle2': yearStyle2,
                'yearStyle3': yearStyle3,
                'yearStyle4': yearStyle4,
                'yearCost1': yearCost1,
                'yearCost2': yearCost2,
                'yearCost3': yearCost3,
                'yearCost4': yearCost4,
                'BatteryStyle1': BatteryStyle1,
                'BatteryStyle2': BatteryStyle2,
                'BatteryStyle3': BatteryStyle3,
                'BatteryStyle4': BatteryStyle4,
                'RangeStyle1': RangeStyle1,
                'RangeStyle2': RangeStyle2,
                'RangeStyle3': RangeStyle3,
                'RangeStyle4': RangeStyle4,
                'PowerStyle1': PowerStyle1,
                'PowerStyle2': PowerStyle2,
                'PowerStyle3': PowerStyle3,
                'PowerStyle4': PowerStyle4,
                'hasSearched': hasSearched,
                'v1Link': v1Link,
                'v2Link': v2Link,
                'v3Link': v3Link,
                'v4Link': v4Link,
                'error_message': error_message,
                'success_message': success_message
            }

            template = JINJA_ENVIRONMENT.get_template('comparecar.html')
            self.response.write(template.render(template_values))

        # CALCULATE IF THERE IS AN INPUT IN VEHICLE 3 AND NONE IN 4
        elif vehicle_3 != "" and vehicle_4 == "":

            vrv = VehicleResultValues()
            vr = VehicleResult()
            v4 = vr
            v4Link = False

            if len(v1_total_query) != 1:
                v1 = vrv
                v1Link = False

            if len(v2_total_query) != 1:
                v2 = vrv
                v2Link = False

            if len(v3_total_query) != 1:
                v3 = vrv
                v3Link = False

            # YEAR LOGIC CALCULATION
            my_list = [v1.year, v2.year, v3.year]
            max_value = max(my_list)
            max_index = my_list.index(max_value)
            min_value = min(i for i in my_list if i > 0)
            min_index = my_list.index(min_value)

            # COST MIN AND MAX
            my_cost_list = [v1.cost, v2.cost, v3.cost]
            max_cost_value = max(my_cost_list)
            max_cost_index = my_cost_list.index(max_cost_value)
            min_cost_value = min(i for i in my_cost_list if i > 0)
            min_cost_index = my_cost_list.index(min_cost_value)

            # BATTERY SIZE MIN AND MAX
            my_battery_list = [v1.batterySize, v2.batterySize, v3.batterySize]
            max_battery_value = max(my_battery_list)
            max_battery_index = my_battery_list.index(max_battery_value)
            min_battery_value = min(i for i in my_battery_list if i > 0)
            min_battery_index = my_battery_list.index(min_battery_value)

            # WLTP RANGE MIN AND MAX
            my_range_list = [v1.WLTP_range, v2.WLTP_range, v3.WLTP_range]
            max_range_value = max(my_range_list)
            max_range_index = my_range_list.index(max_range_value)
            min_range_value = min(i for i in my_range_list if i > 0)
            min_range_index = my_range_list.index(min_range_value)

            # POWER MIN AND MAX
            my_power_list = [v1.power, v2.power, v3.power]
            max_power_value = max(my_power_list)
            max_power_index = my_power_list.index(max_power_value)
            min_power_value = min(i for i in my_power_list if i > 0)
            min_power_index = my_power_list.index(min_power_value)

            self.response.write('</br>Max Index = ' + str(max_power_index))
            self.response.write('</br>Max Power = ' + str(max_power_value))
            self.response.write('</br>Min Index = ' + str(min_power_index))
            self.response.write('</br>Min Power = ' + str(min_power_value))

            # YEAR LOGICAL STYLING
            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
                yearStyle3 = 'text-success font-weight-bold'
            elif max_index == 0:
                yearStyle1 = 'text-success font-weight-bold'
            elif max_index == 1:
                yearStyle2 = 'text-success font-weight-bold'
            elif max_index == 2:
                yearStyle3 = 'text-success font-weight-bold'
            elif max_index == 3:
                yearStyle4 = 'text-success font-weight-bold'

            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
            elif min_index == 0:
                yearStyle1 = 'text-danger font-weight-bold'
            elif min_index == 1:
                yearStyle2 = 'text-danger font-weight-bold'
            elif min_index == 2:
                yearStyle3 = 'text-danger font-weight-bold'
            elif min_index == 3:
                yearStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                yearStyle3 = ''

            # COST LOGIC FOR STYLING
            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
                yearCost3 = 'text-success font-weight-bold'
            elif max_cost_index == 0:
                yearCost1 = 'text-danger font-weight-bold'
            elif max_cost_index == 1:
                yearCost2 = 'text-danger font-weight-bold'
            elif max_cost_index == 2:
                yearCost3 = 'text-danger font-weight-bold'
            elif max_cost_index == 3:
                yearCost4 = 'text-danger font-weight-bold'

            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
                yearCost3 = 'text-success font-weight-bold'
            elif min_cost_index == 0:
                yearCost1 = 'text-success font-weight-bold'
            elif min_cost_index == 1:
                yearCost2 = 'text-success font-weight-bold'
            elif min_cost_index == 2:
                yearCost3 = 'text-success font-weight-bold'
            elif min_cost_index == 3:
                yearCost4 = 'text-success font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearCost1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearCost2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                yearCost3 = ''

            # BATTERY LOGIC FOR STYLING
            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
                BatteryStyle3 = 'text-success font-weight-bold'
            elif max_battery_index == 0:
                BatteryStyle1 = 'text-success font-weight-bold'
            elif max_battery_index == 1:
                BatteryStyle2 = 'text-success font-weight-bold'
            elif max_battery_index == 2:
                BatteryStyle3 = 'text-success font-weight-bold'
            elif max_battery_index == 3:
                BatteryStyle4 = 'text-success font-weight-bold'

            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
                BatteryStyle3 = 'text-success font-weight-bold'
            elif min_battery_index == 0:
                BatteryStyle1 = 'text-danger font-weight-bold'
            elif min_battery_index == 1:
                BatteryStyle2 = 'text-danger font-weight-bold'
            elif min_battery_index == 2:
                BatteryStyle3 = 'text-danger font-weight-bold'
            elif min_battery_index == 3:
                BatteryStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                BatteryStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                BatteryStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                BatteryStyle3 = ''

            # WLTP RANGE FOR STYLING
            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
                RangeStyle3 = 'text-success font-weight-bold'
            elif max_range_index == 0:
                RangeStyle1 = 'text-success font-weight-bold'
            elif max_range_index == 1:
                RangeStyle2 = 'text-success font-weight-bold'
            elif max_range_index == 2:
                RangeStyle3 = 'text-success font-weight-bold'
            elif max_range_index == 3:
                RangeStyle4 = 'text-success font-weight-bold'

            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
                RangeStyle3 = 'text-success font-weight-bold'
            elif min_range_index == 0:
                RangeStyle1 = 'text-danger font-weight-bold'
            elif min_range_index == 1:
                RangeStyle2 = 'text-danger font-weight-bold'
            elif min_range_index == 2:
                RangeStyle3 = 'text-danger font-weight-bold'
            elif min_range_index == 3:
                RangeStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                RangeStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                RangeStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                RangeStyle3 = ''

            # POWER FOR STYLING
            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
                PowerStyle3 = 'text-success font-weight-bold'
            elif max_power_index == 0:
                PowerStyle1 = 'text-success font-weight-bold'
            elif max_power_index == 1:
                PowerStyle2 = 'text-success font-weight-bold'
            elif max_power_index == 2:
                PowerStyle3 = 'text-success font-weight-bold'
            elif max_power_index == 3:
                PowerStyle4 = 'text-success font-weight-bold'

            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
                PowerStyle3 = 'text-success font-weight-bold'
            elif min_power_index == 0:
                PowerStyle1 = 'text-danger font-weight-bold'
            elif min_power_index == 1:
                PowerStyle2 = 'text-danger font-weight-bold'
            elif min_power_index == 2:
                PowerStyle3 = 'text-danger font-weight-bold'
            elif min_power_index == 3:
                PowerStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                PowerStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                PowerStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                PowerStyle3 = ''

            template_values = {
                'user': user,
                'url': url,
                'login_status': login_status,
                'v1': v1,
                'v2': v2,
                'v3': v3,
                'v4': v4,
                'yearStyle1': yearStyle1,
                'yearStyle2': yearStyle2,
                'yearStyle3': yearStyle3,
                'yearStyle4': yearStyle4,
                'yearCost1': yearCost1,
                'yearCost2': yearCost2,
                'yearCost3': yearCost3,
                'yearCost4': yearCost4,
                'BatteryStyle1': BatteryStyle1,
                'BatteryStyle2': BatteryStyle2,
                'BatteryStyle3': BatteryStyle3,
                'BatteryStyle4': BatteryStyle4,
                'RangeStyle1': RangeStyle1,
                'RangeStyle2': RangeStyle2,
                'RangeStyle3': RangeStyle3,
                'RangeStyle4': RangeStyle4,
                'PowerStyle1': PowerStyle1,
                'PowerStyle2': PowerStyle2,
                'PowerStyle3': PowerStyle3,
                'PowerStyle4': PowerStyle4,
                'hasSearched': hasSearched,
                'v1Link': v1Link,
                'v2Link': v2Link,
                'v3Link': v3Link,
                'v4Link': v4Link,
                'error_message': error_message,
                'success_message': success_message
            }

            template = JINJA_ENVIRONMENT.get_template('comparecar.html')
            self.response.write(template.render(template_values))

        # CALCULATE IF THERE IS NO INPUT IN VEHICLE 3 BUT THERE IS AN INPUT IN 4
        elif vehicle_3 == "" and vehicle_4 != "":
            vrv = VehicleResultValues()
            vr = VehicleResult()
            v3 = vr
            v3Link = False

            if len(v1_total_query) != 1:
                v1 = vrv
                v1Link = False

            if len(v2_total_query) != 1:
                v2 = vrv
                v2Link = False

            if len(v4_total_query) != 1:
                v4 = vrv
                v4Link = False

            # YEAR MIN MAX
            my_list = [v1.year, v2.year, 0, v4.year]
            max_value = max(my_list)
            max_index = my_list.index(max_value)
            min_value = min(i for i in my_list if i > 0)
            min_index = my_list.index(min_value)

            # COST MIN AND MAX
            my_cost_list = [v1.cost, v2.cost, 0, v4.cost]
            max_cost_value = max(my_cost_list)
            max_cost_index = my_cost_list.index(max_cost_value)
            min_cost_value = min(i for i in my_cost_list if i > 0)
            min_cost_index = my_cost_list.index(min_cost_value)

            # BATTERY SIZE MIN AND MAX
            my_battery_list = [v1.batterySize, v2.batterySize, 0, v4.batterySize]
            max_battery_value = max(my_battery_list)
            max_battery_index = my_battery_list.index(max_battery_value)
            min_battery_value = min(i for i in my_battery_list if i > 0)
            min_battery_index = my_battery_list.index(min_battery_value)

            # WLTP RANGE MIN AND MAX
            my_range_list = [v1.WLTP_range, v2.WLTP_range, 0, v4.WLTP_range]
            max_range_value = max(my_range_list)
            max_range_index = my_range_list.index(max_range_value)
            min_range_value = min(i for i in my_range_list if i > 0)
            min_range_index = my_range_list.index(min_range_value)

            # POWER MIN AND MAX
            my_power_list = [v1.power, v2.power, 0, v4.power]
            max_power_value = max(my_power_list)
            max_power_index = my_power_list.index(max_power_value)
            min_power_value = min(i for i in my_power_list if i > 0)
            min_power_index = my_power_list.index(min_power_value)

            self.response.write('</br>Max Index = ' + str(max_power_index))
            self.response.write('</br>Max Power = ' + str(max_power_value))
            self.response.write('</br>Min Index = ' + str(min_power_index))
            self.response.write('</br>Min Power = ' + str(min_power_value))

            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
                yearStyle4 = 'text-success font-weight-bold'
            elif max_index == 0:
                yearStyle1 = 'text-success font-weight-bold'
            elif max_index == 1:
                yearStyle2 = 'text-success font-weight-bold'
            elif max_index == 2:
                yearStyle3 = 'text-success font-weight-bold'
            elif max_index == 3:
                yearStyle4 = 'text-success font-weight-bold'

            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
                yearStyle4 = 'text-success font-weight-bold'
            elif min_index == 0:
                yearStyle1 = 'text-danger font-weight-bold'
            elif min_index == 1:
                yearStyle2 = 'text-danger font-weight-bold'
            elif min_index == 2:
                yearStyle3 = 'text-danger font-weight-bold'
            elif min_index == 3:
                yearStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearStyle2 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                yearStyle4 = ''

            # COST LOGIC FOR STYLING
            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
                yearCost4 = 'text-success font-weight-bold'
            elif max_cost_index == 0:
                yearCost1 = 'text-danger font-weight-bold'
            elif max_cost_index == 1:
                yearCost2 = 'text-danger font-weight-bold'
            elif max_cost_index == 2:
                yearCost3 = 'text-danger font-weight-bold'
            elif max_cost_index == 3:
                yearCost4 = 'text-danger font-weight-bold'

            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
                yearCost4 = 'text-success font-weight-bold'
            elif min_cost_index == 0:
                yearCost1 = 'text-success font-weight-bold'
            elif min_cost_index == 1:
                yearCost2 = 'text-success font-weight-bold'
            elif min_cost_index == 2:
                yearCost3 = 'text-success font-weight-bold'
            elif min_cost_index == 3:
                yearCost4 = 'text-success font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearCost1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearCost2 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                yearCost4 = ''

            # BATTERY LOGIC FOR STYLING
            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
                BatteryStyle4 = 'text-success font-weight-bold'
            elif max_battery_index == 0:
                BatteryStyle1 = 'text-success font-weight-bold'
            elif max_battery_index == 1:
                BatteryStyle2 = 'text-success font-weight-bold'
            elif max_battery_index == 2:
                BatteryStyle3 = 'text-success font-weight-bold'
            elif max_battery_index == 3:
                BatteryStyle4 = 'text-success font-weight-bold'

            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
                BatteryStyle4 = 'text-success font-weight-bold'
            elif min_battery_index == 0:
                BatteryStyle1 = 'text-danger font-weight-bold'
            elif min_battery_index == 1:
                BatteryStyle2 = 'text-danger font-weight-bold'
            elif min_battery_index == 2:
                BatteryStyle3 = 'text-danger font-weight-bold'
            elif min_battery_index == 3:
                BatteryStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                BatteryStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                BatteryStyle2 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                BatteryStyle4 = ''

            # WLTP RANGE FOR STYLING
            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
                RangeStyle4 = 'text-success font-weight-bold'
            elif max_range_index == 0:
                RangeStyle1 = 'text-success font-weight-bold'
            elif max_range_index == 1:
                RangeStyle2 = 'text-success font-weight-bold'
            elif max_range_index == 2:
                RangeStyle3 = 'text-success font-weight-bold'
            elif max_range_index == 3:
                RangeStyle4 = 'text-success font-weight-bold'

            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
                RangeStyle4 = 'text-success font-weight-bold'
            elif min_range_index == 0:
                RangeStyle1 = 'text-danger font-weight-bold'
            elif min_range_index == 1:
                RangeStyle2 = 'text-danger font-weight-bold'
            elif min_range_index == 2:
                RangeStyle3 = 'text-danger font-weight-bold'
            elif min_range_index == 3:
                RangeStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                RangeStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                RangeStyle2 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                RangeStyle4 = ''

            # POWER FOR STYLING
            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
                PowerStyle4 = 'text-success font-weight-bold'
            elif max_power_index == 0:
                PowerStyle1 = 'text-success font-weight-bold'
            elif max_power_index == 1:
                PowerStyle2 = 'text-success font-weight-bold'
            elif max_power_index == 2:
                PowerStyle3 = 'text-success font-weight-bold'
            elif max_power_index == 3:
                PowerStyle4 = 'text-success font-weight-bold'

            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
                PowerStyle4 = 'text-success font-weight-bold'
            elif min_power_index == 0:
                PowerStyle1 = 'text-danger font-weight-bold'
            elif min_power_index == 1:
                PowerStyle2 = 'text-danger font-weight-bold'
            elif min_power_index == 2:
                PowerStyle3 = 'text-danger font-weight-bold'
            elif min_power_index == 3:
                PowerStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                PowerStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                PowerStyle2 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                PowerStyle4 = ''

            template_values = {
                'user': user,
                'url': url,
                'login_status': login_status,
                'v1': v1,
                'v2': v2,
                'v3': v3,
                'v4': v4,
                'yearStyle1': yearStyle1,
                'yearStyle2': yearStyle2,
                'yearStyle3': yearStyle3,
                'yearStyle4': yearStyle4,
                'yearCost1': yearCost1,
                'yearCost2': yearCost2,
                'yearCost3': yearCost3,
                'yearCost4': yearCost4,
                'BatteryStyle1': BatteryStyle1,
                'BatteryStyle2': BatteryStyle2,
                'BatteryStyle3': BatteryStyle3,
                'BatteryStyle4': BatteryStyle4,
                'RangeStyle1': RangeStyle1,
                'RangeStyle2': RangeStyle2,
                'RangeStyle3': RangeStyle3,
                'RangeStyle4': RangeStyle4,
                'PowerStyle1': PowerStyle1,
                'PowerStyle2': PowerStyle2,
                'PowerStyle3': PowerStyle3,
                'PowerStyle4': PowerStyle4,
                'hasSearched': hasSearched,
                'v1Link': v1Link,
                'v2Link': v2Link,
                'v3Link': v3Link,
                'v4Link': v4Link,
                'error_message': error_message,
                'success_message': success_message
            }

            template = JINJA_ENVIRONMENT.get_template('comparecar.html')
            self.response.write(template.render(template_values))

        # CALCULATE IF THERE IS AN INPUT IN BOTH VEHICLE 3 AND 4
        elif vehicle_3 != "" and vehicle_4 != "":
            vrv = VehicleResultValues()
            vr = VehicleResult()

            if len(v1_total_query) != 1:
                v1 = vrv
                v1Link = False

            if len(v2_total_query) != 1:
                v2 = vrv
                v2Link = False

            if len(v3_total_query) != 1:
                v3 = vrv
                v3Link = False

            if len(v4_total_query) != 1:
                v4 = vrv
                v4Link = False


            my_list = [v1.year, v2.year, v3.year, v4.year]
            max_value = max(my_list)
            max_index = my_list.index(max_value)
            min_value = min(i for i in my_list if i > 0)
            min_index = my_list.index(min_value)

            # COST MIN AND MAX
            my_cost_list = [v1.cost, v2.cost, v3.cost, v4.cost]
            max_cost_value = max(my_cost_list)
            max_cost_index = my_cost_list.index(max_cost_value)
            min_cost_value = min(i for i in my_cost_list if i > 0)
            min_cost_index = my_cost_list.index(min_cost_value)

            # BATTERY SIZE MIN AND MAX
            my_battery_list = [v1.batterySize, v2.batterySize, v3.batterySize, v4.batterySize]
            max_battery_value = max(my_battery_list)
            max_battery_index = my_battery_list.index(max_battery_value)
            min_battery_value = min(i for i in my_battery_list if i > 0)
            min_battery_index = my_battery_list.index(min_battery_value)

            # WLTP RANGE MIN AND MAX
            my_range_list = [v1.WLTP_range, v2.WLTP_range, v3.WLTP_range, v4.WLTP_range]
            max_range_value = max(my_range_list)
            max_range_index = my_range_list.index(max_range_value)
            min_range_value = min(i for i in my_range_list if i > 0)
            min_range_index = my_range_list.index(min_range_value)

            # POWER MIN AND MAX
            my_power_list = [v1.power, v2.power, v3.power, v4.power]
            max_power_value = max(my_power_list)
            max_power_index = my_power_list.index(max_power_value)
            min_power_value = min(i for i in my_power_list if i > 0)
            min_power_index = my_power_list.index(min_power_value)

            self.response.write('</br>Max Index = ' + str(max_power_index))
            self.response.write('</br>Max Power = ' + str(max_power_value))
            self.response.write('</br>Min Index = ' + str(min_power_index))
            self.response.write('</br>Min Power = ' + str(min_power_value))

            # YEAR LOGICAL STYLING
            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
                yearStyle3 = 'text-success font-weight-bold'
                yearStyle4 = 'text-success font-weight-bold'
            elif max_index == 0:
                yearStyle1 = 'text-success font-weight-bold'
            elif max_index == 1:
                yearStyle2 = 'text-success font-weight-bold'
            elif max_index == 2:
                yearStyle3 = 'text-success font-weight-bold'
            elif max_index == 3:
                yearStyle4 = 'text-success font-weight-bold'

            if max_index == min_index:
                yearStyle1 = 'text-success font-weight-bold'
                yearStyle2 = 'text-success font-weight-bold'
                yearStyle3 = 'text-success font-weight-bold'
                yearStyle4 = 'text-success font-weight-bold'
            elif min_index == 0:
                yearStyle1 = 'text-danger font-weight-bold'
            elif min_index == 1:
                yearStyle2 = 'text-danger font-weight-bold'
            elif min_index == 2:
                yearStyle3 = 'text-danger font-weight-bold'
            elif min_index == 3:
                yearStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                yearStyle3 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                yearStyle4 = ''

            # COST LOGIC FOR STYLING
            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
                yearCost3 = 'text-success font-weight-bold'
                yearCost4 = 'text-success font-weight-bold'
            elif max_cost_index == 0:
                yearCost1 = 'text-danger font-weight-bold'
            elif max_cost_index == 1:
                yearCost2 = 'text-danger font-weight-bold'
            elif max_cost_index == 2:
                yearCost3 = 'text-danger font-weight-bold'
            elif max_cost_index == 3:
                yearCost4 = 'text-danger font-weight-bold'

            if max_cost_index == min_cost_index:
                yearCost1 = 'text-success font-weight-bold'
                yearCost2 = 'text-success font-weight-bold'
                yearCost3 = 'text-success font-weight-bold'
                yearCost4 = 'text-success font-weight-bold'
            elif min_cost_index == 0:
                yearCost1 = 'text-success font-weight-bold'
            elif min_cost_index == 1:
                yearCost2 = 'text-success font-weight-bold'
            elif min_cost_index == 2:
                yearCost3 = 'text-success font-weight-bold'
            elif min_cost_index == 3:
                yearCost4 = 'text-success font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                yearCost1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                yearCost2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                yearCost3 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                yearCost4 = ''

            # BATTERY LOGIC FOR STYLING
            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
                BatteryStyle3 = 'text-success font-weight-bold'
                BatteryStyle4 = 'text-success font-weight-bold'
            elif max_battery_index == 0:
                BatteryStyle1 = 'text-success font-weight-bold'
            elif max_battery_index == 1:
                BatteryStyle2 = 'text-success font-weight-bold'
            elif max_battery_index == 2:
                BatteryStyle3 = 'text-success font-weight-bold'
            elif max_battery_index == 3:
                BatteryStyle4 = 'text-success font-weight-bold'

            if max_battery_index == min_battery_index:
                BatteryStyle1 = 'text-success font-weight-bold'
                BatteryStyle2 = 'text-success font-weight-bold'
                BatteryStyle3 = 'text-success font-weight-bold'
                BatteryStyle4 = 'text-success font-weight-bold'
            elif min_battery_index == 0:
                BatteryStyle1 = 'text-danger font-weight-bold'
            elif min_battery_index == 1:
                BatteryStyle2 = 'text-danger font-weight-bold'
            elif min_battery_index == 2:
                BatteryStyle3 = 'text-danger font-weight-bold'
            elif min_battery_index == 3:
                BatteryStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                BatteryStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                BatteryStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                BatteryStyle3 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                BatteryStyle4 = ''

            # WLTP RANGE FOR STYLING
            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
                RangeStyle3 = 'text-success font-weight-bold'
                RangeStyle4 = 'text-success font-weight-bold'
            elif max_range_index == 0:
                RangeStyle1 = 'text-success font-weight-bold'
            elif max_range_index == 1:
                RangeStyle2 = 'text-success font-weight-bold'
            elif max_range_index == 2:
                RangeStyle3 = 'text-success font-weight-bold'
            elif max_range_index == 3:
                RangeStyle4 = 'text-success font-weight-bold'

            if max_range_index == min_range_index:
                RangeStyle1 = 'text-success font-weight-bold'
                RangeStyle2 = 'text-success font-weight-bold'
                RangeStyle3 = 'text-success font-weight-bold'
                RangeStyle4 = 'text-success font-weight-bold'
            elif min_range_index == 0:
                RangeStyle1 = 'text-danger font-weight-bold'
            elif min_range_index == 1:
                RangeStyle2 = 'text-danger font-weight-bold'
            elif min_range_index == 2:
                RangeStyle3 = 'text-danger font-weight-bold'
            elif min_range_index == 3:
                RangeStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                RangeStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                RangeStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                RangeStyle3 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                RangeStyle4 = ''

            # POWER FOR STYLING
            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
                PowerStyle3 = 'text-success font-weight-bold'
                PowerStyle4 = 'text-success font-weight-bold'
            elif max_power_index == 0:
                PowerStyle1 = 'text-success font-weight-bold'
            elif max_power_index == 1:
                PowerStyle2 = 'text-success font-weight-bold'
            elif max_power_index == 2:
                PowerStyle3 = 'text-success font-weight-bold'
            elif max_power_index == 3:
                PowerStyle4 = 'text-success font-weight-bold'

            if max_power_index == min_power_index:
                PowerStyle1 = 'text-success font-weight-bold'
                PowerStyle2 = 'text-success font-weight-bold'
                PowerStyle3 = 'text-success font-weight-bold'
                PowerStyle4 = 'text-success font-weight-bold'
            elif min_power_index == 0:
                PowerStyle1 = 'text-danger font-weight-bold'
            elif min_power_index == 1:
                PowerStyle2 = 'text-danger font-weight-bold'
            elif min_power_index == 2:
                PowerStyle3 = 'text-danger font-weight-bold'
            elif min_power_index == 3:
                PowerStyle4 = 'text-danger font-weight-bold'

            if len(v1_total_query) != 1:
                v1 = vr
                PowerStyle1 = ''

            if len(v2_total_query) != 1:
                v2 = vr
                PowerStyle2 = ''

            if len(v3_total_query) != 1:
                v3 = vr
                PowerStyle3 = ''

            if len(v4_total_query) != 1:
                v4 = vr
                PowerStyle4 = ''

            template_values = {
                'user': user,
                'url': url,
                'login_status': login_status,
                'v1': v1,
                'v2': v2,
                'v3': v3,
                'v4': v4,
                'yearStyle1': yearStyle1,
                'yearStyle2': yearStyle2,
                'yearStyle3': yearStyle3,
                'yearStyle4': yearStyle4,
                'yearCost1': yearCost1,
                'yearCost2': yearCost2,
                'yearCost3': yearCost3,
                'yearCost4': yearCost4,
                'BatteryStyle1': BatteryStyle1,
                'BatteryStyle2': BatteryStyle2,
                'BatteryStyle3': BatteryStyle3,
                'BatteryStyle4': BatteryStyle4,
                'RangeStyle1': RangeStyle1,
                'RangeStyle2': RangeStyle2,
                'RangeStyle3': RangeStyle3,
                'RangeStyle4': RangeStyle4,
                'PowerStyle1': PowerStyle1,
                'PowerStyle2': PowerStyle2,
                'PowerStyle3': PowerStyle3,
                'PowerStyle4': PowerStyle4,
                'hasSearched': hasSearched,
                'v1Link': v1Link,
                'v2Link': v2Link,
                'v3Link': v3Link,
                'v4Link': v4Link,
                'error_message': error_message,
                'success_message': success_message
            }

            template = JINJA_ENVIRONMENT.get_template('comparecar.html')
            self.response.write(template.render(template_values))

        else:
            self.response.write('Something is wrong')
