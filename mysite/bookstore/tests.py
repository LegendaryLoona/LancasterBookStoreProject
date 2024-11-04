from django.test import TestCase, RequestFactory
import json
from . import views, models

class Main_test(TestCase):

    models.Book.objects.create(name="lion", author="roar")
    models.Book.objects.create(name="cat", author="meow")

    factory = RequestFactory()
    request = factory.get('/book/library')
    response = views.library(request)

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_list(self):
        response_data = json.loads(self.response.content)
        print("New data:   ", response_data)
        self.assertIsInstance(response_data, list)
