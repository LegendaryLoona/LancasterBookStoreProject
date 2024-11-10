from django.db import models


class Book(models.Model):
    bid = models.IntegerField(default=None)
    name = models.CharField(max_length=50, default=None)
    author = models.CharField(max_length=50, default=None)
    price = models.FloatField(max_length=6, default=None)
    edition = models.CharField(max_length=10, default=None)
    description = models.TextField(default=None)

class Author(models.Model):
    aid = models.IntegerField(default=None)
    name = models.CharField(max_length=50, default=None)
    list_of_books = models.TextField(default=None)
