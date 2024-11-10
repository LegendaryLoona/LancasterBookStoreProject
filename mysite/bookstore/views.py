from django.shortcuts import render
from .models import Book, Author
from django.http import JsonResponse

def library(request):
    author_filter = request.GET.get('author')
    list_book = Book.objects.all().values('id', 'name', 'author', 'price', 'edition', 'description')
    if author_filter:
        list_book = list_book.filter(author__icontains=author_filter)
    return JsonResponse(list(list_book), safe=False)

def addauthor(request):
    author_name = request.GET.get('name')
    if not author_name or any(not c.isalnum() and not c ==" " for c in author_name):
        return JsonResponse("Please provide a valid name", safe=False)
    else:
        Author.objects.create(name=author_name, list_of_books="")
        return JsonResponse("Author added successfully", safe=False)
    
def addbook(request):
    book_name = request.GET.get('name')
    author_name = request.GET.get('author')
    book_price = request.GET.get('price')
    book_edition = request.GET.get('edition')
    book_description = request.GET.get('description')

    try:
        author = Author.objects.get(name = author_name)
    except: 
        return JsonResponse("Please provide a valid author", safe=False)
    try:
        float(book_price)
    except:
        return JsonResponse("Please provide a valid price", safe=False)
    
    if  not (book_name and author_name and book_price and book_edition and book_description):
        return JsonResponse("Please provide all of the attributes", safe=False)

    else:
        Book.objects.create(name=book_name, author=author_name, price = book_price, edition=book_edition, description=book_description)
        author.list_of_books += book_name + ", "
        author.save()
        return JsonResponse("Book added successfully", safe=False)

    
