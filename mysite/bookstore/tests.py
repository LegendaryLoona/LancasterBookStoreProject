from django.test import TestCase, RequestFactory
from . import views, models

class Main_test(TestCase):
    factory = RequestFactory()
    request = factory.get('/book/library')
    response = views.library(request)

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)