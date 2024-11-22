from .models import Book, Author
from django.http import JsonResponse
from django.db.models import Q

def edit_author(request):
    current_name = request.GET.get('current_name')
    new_name = request.GET.get('new_name')

    if not current_name or not new_name:
        return JsonResponse("Please provide both the current name and a new name", safe=False)
    if any(not c.isalnum() and c != " " for c in new_name):
        return JsonResponse("Please provide a valid name", safe=False)
    try:
        author = Author.objects.get(author_name=current_name)
    except Author.DoesNotExist:
        return JsonResponse("Author not found", safe=False)
    author.author_name = new_name
    author.save()
    return JsonResponse("Author updated successfully", safe=False)

def edit_book(request):
    book_id = request.GET.get('book_id')
    new_name = request.GET.get('name')
    new_price = request.GET.get('price')
    new_edition = request.GET.get('edition')
    new_description = request.GET.get('description')
    new_author_name = request.GET.get('author')
    
    try:
        int(book_id)
    except:
        return JsonResponse("Please provide a valid book ID", safe=False)
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse("Book not found", safe=False)
    try:
        float(new_price)
    except:
        return JsonResponse("Please provide a valid price", safe=False)
    if new_name:
        book.name = new_name
    if new_price:
            book.price = float(new_price)
    if new_edition:
        book.edition = new_edition
    if new_description:
        book.description = new_description
    if new_author_name:
        book.author.clear()
        author_names = [name.strip() for name in new_author_name.split(",")]
        for name in author_names:
            new_author_name, created = Author.objects.get_or_create(author_name=name)
            book.author.add(new_author_name)
    book.save()
    return JsonResponse("Book updated successfully", safe=False)

def addauthor(request):
    author_name = request.GET.get('name')
    author = Author.objects.filter(author_name=author_name)
    if author.exists():
        return JsonResponse("Author already exists", safe=False)
    if not author_name or any(not c.isalnum() and not c ==" " for c in author_name):
        return JsonResponse("Please provide a valid name", safe=False)
    else:
        Author.objects.create(author_name=author_name)
        return JsonResponse("Author added successfully", safe=False)
    
def addbook(request):
    book_name = request.GET.get('name')
    author_name = request.GET.get('author')
    book_price = request.GET.get('price')
    book_edition = request.GET.get('edition')
    book_description = request.GET.get('description')

    try:
        float(book_price)
    except:
        return JsonResponse("Please provide a valid price", safe=False)
    if  not (book_name and author_name and book_price and book_edition and book_description):
        return JsonResponse("Please provide all of the attributes", safe=False)
    author_names = [name.strip() for name in author_name.split(",")]
    existing_books = Book.objects.filter( name=book_name,price=book_price,edition=book_edition,description=book_description)
    for book in existing_books:
        existing_authors = set(book.author.values_list('author_name', flat=True))
        if existing_authors == set(author_names):
            return JsonResponse("Book already exists", safe=False)
    book = Book.objects.create(
        name=book_name,  
        price=book_price,
        edition=book_edition,
        description=book_description
        )
    for name in author_names:
        author, created = Author.objects.get_or_create(author_name=name)
        book.author.add(author)
    return JsonResponse("Book added successfully", safe=False)
    
def delete_author(request):
    author_id = request.GET.get('id')
    try:
        int(author_id)
    except ValueError:
        return JsonResponse( "Invalid author ID.", safe=False)
    author_to_delete = Author.objects.filter(id=author_id)
    if author_to_delete.exists():
        author_to_delete.delete()
        return JsonResponse( f"Author with ID {author_id} deleted successfully.", safe=False)
    else:
        return JsonResponse("author not found.", safe=False)

def delete_book(request):
        book_id = request.GET.get('id')
        try:
            int(book_id)
        except ValueError:
            return JsonResponse( "Invalid book ID.", safe=False)
        books_to_delete = Book.objects.filter(id=book_id)
        if books_to_delete.exists():
            books_to_delete.delete()
            return JsonResponse( f"Book with ID {book_id} deleted successfully.", safe=False)
        else:
            return JsonResponse("Book not found.", safe=False)

def sort_alph(request):
    list_book = Book.objects.all().prefetch_related('author').values('id', 'name', 'author__author_name','price','edition','description')
    if request.GET.get('order') == "desc":
        sorted_data = sorted(list_book, key=lambda x: x["name"], reverse=True)
    else:
        sorted_data = sorted(list_book, key=lambda x: x["name"])
    return JsonResponse(sorted_data, safe=False)

def sort_price(request):
    list_book = Book.objects.all().prefetch_related('author').values('id', 'name', 'author__author_name','price','edition','description')
    if request.GET.get('order') == "desc":
        sorted_data = sorted(list_book, key=lambda x: x["price"], reverse=True)
    else:
        sorted_data = sorted(list_book, key=lambda x: x["price"])
    return JsonResponse(sorted_data, safe=False)

def search_book(request):
    book_name = request.GET.get('name')
    try:
        words = book_name.split()
    except:
        words = ""
    query = Q()
    for word in words:
        query &= Q(name__icontains=word) 
    results = Book.objects.filter(query).prefetch_related('author').values('id', 'name', 'author__author_name','price','edition','description')
    if not results.exists():
        return JsonResponse("Book not found.", safe=False)
    return JsonResponse(list(results), safe=False)

def search_author(request):
    authorname= request.GET.get("name")
    try:
        words = authorname.split()
    except:
        words = ""
    query = Q()
    for word in words:
        query &= Q(author_name__icontains=word) 
    results = Author.objects.filter(query)
    response_data = []
    for author in results:
        response_data.append({
            "author_id" :author.id,
            'author_name': author.author_name,
            'books': author.list_of_books() 
        })
    return JsonResponse(response_data, safe=False)                       
        
