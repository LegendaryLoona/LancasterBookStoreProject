from django.test import TestCase, RequestFactory
import json
from . import views, models

class Main_test(TestCase):

    # models.Book.objects.create(name="lion", author="roar")
    # models.Book.objects.create(name="cat", author="meow")

    def setUp(self):
        models.Book.objects.create(name="Sample Book 1", author="Jalal")
        models.Book.objects.create(name="Sample Book 2", author="Jalal")
        models.Book.objects.create(name="Sample Book 3", author="Another Author")


    def test_response(self):
        factory = RequestFactory()
        request = factory.get('/book/library')
        response = views.library(request)
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        factory = RequestFactory()
        request = factory.get('/book/library')
        response = views.library(request)
        response_data = json.loads(response.content)
        print("New data:   ", response_data)
        self.assertIsInstance(response_data, list)
    
    def test_filter(self):
        factory = RequestFactory()
        filter_request = factory.get('/book/library/?author=Jalal')
        filter_response = views.library(filter_request)
        response_data = json.loads(filter_response.content)
        print("Jalal books3:   ", response_data)
        for i in response_data:
            self.assertEqual(i['author'], "Jalal")

    # models.Book.objects.filter(name="lion").delete()
    # models.Book.objects.filter(name="cat").delete()
