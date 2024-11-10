from django.db import models


class Book(models.Model):
    # bid = models.IntegerField(default="")
    name = models.CharField(max_length=50, default="")
    author = models.CharField(max_length=50, default="")
    price = models.FloatField(max_length=6, default="")
    edition = models.CharField(max_length=10, default="")
    description = models.TextField(default="")

class Author(models.Model):
    # aid = models.IntegerField(default="")
    name = models.CharField(max_length=50, default="")
    list_of_books = models.TextField(default="")
