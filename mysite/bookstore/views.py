from django.shortcuts import render
from .models import Book
from django.http import JsonResponse

def library(request):

    list_book = list(Book.objects.all().values('id', 'name', 'author'))
    return JsonResponse(list_book, safe=False)

    
