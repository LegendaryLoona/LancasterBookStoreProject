from django.shortcuts import render
from .models import Book
from django.http import JsonResponse

def library(request):
    author_filter = request.GET.get('author')
    list_book = Book.objects.all().values('id', 'name', 'author')
    if author_filter:
        list_book = list_book.filter(author__icontains=author_filter)
    return JsonResponse(list(list_book), safe=False)

    
