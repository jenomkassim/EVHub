import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from review import ReviewAndRating
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
        car_deets2 = ndb.Key('Vehicles', car_id)

        # self.response.out.write(car_deets2)

        query = Vehicles.query(ancestor=car_deets2)
        j = ''

        # self.response.out.write(names)

        # greetings = Vehicles.query(car_deets2).fetch()

        # for greeting in greetings:
        #     self.response.out.write(greeting.name)

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'car_deets': car_deets,
            'idd': idd,
            'error_message': error_message,
            'query': query,
            'j': j
        }

        template = JINJA_ENVIRONMENT.get_template('car-details.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        login_status = ''
        error_message = ''
        success_message = ''
        review_message = ''
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

        if action == 'Review':
            # user_review = self.request.get('user_review')
            # user_rating = self.request.get('rating')
            # self.response.write(user_review)
            # self.response.write('</br>' + user_rating)

            new_review = ReviewAndRating(
                review=self.request.get('user_review'),
                rating=int(self.request.get('rating'))
            )

            car_deets.review.append(new_review)
            car_deets.put()
            self.redirect('/car-details?id=' + str(idd))

        if action == 'Delete Review':
            index = int(self.request.get('index'))

            # user = users.get_current_user()
            # myuser_key = ndb.Key('MyUser', user.user_id())
            # myuser = myuser_key.get()

            del car_deets.review[index]
            car_deets.put()
            review_message = 'Review Deleted'

            self.redirect('/car-details?id=' + str(idd))

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'car_deets': car_deets,
            'idd': idd,
            'error_message': error_message,
            'success_message': success_message,
            'review_message': review_message
        }

        template = JINJA_ENVIRONMENT.get_template('car-details.html')
        self.response.write(template.render(template_values))
