from django.db import models

class Author(models.Model):
    author_name = models.CharField(max_length=50, default=None)
    # list_of_books = models.TextField(default=None)
    @property
    def list_of_books(self):
        return [book.name for book in self.books.all()]



class Book(models.Model):
    name = models.CharField(max_length=50, default=None)
    # author = models.CharField(max_length=50, default=None)
    # author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    author = models.ManyToManyField(Author, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 ) 
    edition = models.CharField(max_length=10, default=None)
    description = models.TextField(default=None)
