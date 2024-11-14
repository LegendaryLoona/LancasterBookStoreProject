from django.test import TestCase, RequestFactory
import json
from . import views, models

class Main_test(TestCase):

    # models.Book.objects.create(name="lion", author="roar")
    # models.Book.objects.create(name="cat", author="meow")

    def setUp(self):
        models.Author.objects.create(name="Jalal", list_of_books="Sample Book 1, Sample Book 2")
        models.Author.objects.create(name="Another Author", list_of_books="Sample Book 3")
        models.Book.objects.create(name="Sample Book 1", author="Jalal", edition = 1, price = 123, description = "new description",)
        models.Book.objects.create(name="Sample Book 2", author="Jalal", edition = 1, price = 123, description = "new description",)
        models.Book.objects.create(name="Sample Book 3", author="Another Author", edition = 1, price = 123, description = "new description",)

    def test_response(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = views.library(request)
        self.assertEqual(response.status_code, 200)

    def test_list(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = views.library(request)
        response_data = json.loads(response.content)
        # print("New data:   ", response_data)
        self.assertIsInstance(response_data, list)

    def test_filter(self):
        factory = RequestFactory()
        filter_request = factory.get('/?author=Jalal')
        filter_response = views.library(filter_request)
        response_data = json.loads(filter_response.content)
        print("Jalal books3:   ", response_data)
        for i in response_data:
            self.assertEqual(i['author'], "Jalal")


    def test_addbook(self):
        expected_book = {
            'id': 4,
            'name': "Sample Book 4",
            'author': "Jalal",
            'edition': '1',
            'price': 123,
            'description': "new description",
        }
        factory = RequestFactory()
        filter_request = factory.get('/?name=Sample Book 4&author=Jalal&edition=1&price=123&description=new description')
        filter_response = views.addbook(filter_request)
        filter_response = views.library(factory.get('/'))
        response_data = json.loads(filter_response.content)
        self.assertIn(expected_book, response_data)


    def test_deletebook(self):
        expected_book = {
            'id': 4,
            'name': "Sample Book 4",
            'author': "Jalal",
            'edition': '1',
            'price': 123,
            'description': "new description",
        }
        factory = RequestFactory()
        filter_request = factory.get('/?name=Sample Book 4&author=Jalal&edition=1&price=123&description=new description')
        filter_response = views.addbook(filter_request)
        filter_response = views.library(factory.get('/'))
        response_data = json.loads(filter_response.content)
        self.assertIn(expected_book, response_data)
        filter_response = views.delete_book(factory.get('/?id=4'))
        filter_response = views.library(factory.get('/'))
        response_data = json.loads(filter_response.content)
        

        self.assertNotIn(expected_book, response_data)
    # models.Book.objects.filter(name="lion").delete()
    # models.Book.objects.filter(name="cat").delete()
