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
        count = 0
        add = 0
        user = users.get_current_user()
        sortedReview = ''

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

        query = Vehicles.query(ancestor=car_deets2)

        j = ''
        finalreview = []

        for a in query:
            for b in a.review:
                count = count + 1
                add = add + float(b.rating)

        if count > 0:
            average = str(round((add / count), 1)) + ' / 10'
        else:
            average = 'No review'

        template_values = {
            'user': user,
            'url': url,
            'login_status': login_status,
            'car_deets': car_deets,
            'idd': idd,
            'error_message': error_message,
            'query': query,
            'j': j,
            'average': average,
            'sortedReview': sortedReview
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

            new_review = ReviewAndRating(
                review=self.request.get('user_review'),
                rating=int(self.request.get('rating'))
            )

            car_deets.review.append(new_review)
            car_deets.put()
            self.redirect('/car-details?id=' + str(idd))

        if action == 'Delete Review':
            index = int(self.request.get('index'))

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
