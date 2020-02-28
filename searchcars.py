





class DisplayCars(webapp2.RequestHandler):
    def get(self):
        search = Vehicles()
        searchResult = search.query()
        for i in searchResult:
            search_result_name = self.response.out.write('Car Name: %s' % i.name)

        template_values = {
            'search_result_name': search_result_name
        }

        template = JINJA_ENVIRONMENT.get_template('addcar.html')
        self.response.write(template.render(template_values))

