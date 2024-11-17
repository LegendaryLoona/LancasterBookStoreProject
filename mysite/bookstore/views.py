from django.shortcuts import render
from .models import Book, Author
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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
        author.list_of_books += book_name + ","
        author.save()
        return JsonResponse("Book added successfully", safe=False)

# Might go very wrong up if we are removing the last book
def delete_book(request):
        book_id = request.GET.get('id')
        if book_id:
            try:
                int(book_id)
            except ValueError:
                return JsonResponse( "Invalid book ID.", safe=False)
            books_to_delete = Book.objects.filter(id=book_id)
            if books_to_delete.exists():
                book_store= get_object_or_404(Book, id=book_id)
                book_info = {
                            'name': book_store.name, 
                            'author': book_store.author if hasattr(Book, 'description') else '',
                            'price': book_store.price if hasattr(Book, 'description') else '',
                            'edition': book_store.edition if hasattr(Book, 'description') else '',
                            'description': book_store.description if hasattr(Book, 'description') else '',
                        }
                author1 = Author.objects.filter(name=book_store.author)
                if author1.exists():
                    author = get_object_or_404(Author, name=book_store.author)
                    # if author.list_of_books.startswith(book_store.name+","):
                    #     author.list_of_books = author.list_of_books.replace(book_store.name+",", "")
                    #     author.list_of_books= author.list_of_books.lstrip()
                    #     author.save()
                    # if ", " +book_store.name+"," in author.list_of_books:
                    #     author.list_of_books = author.list_of_books.replace(", " +book_store.name+",", ",") 
                    #     author.save()
                    old_books = author.list_of_books[:-1].split(",")
                    old_books.remove(book_store.name)
                    author.list_of_books = ",".join(old_books)+","
                    author.save()
                books_to_delete.delete()
                return JsonResponse( f"Book with ID {book_id} deleted successfully.{book_info}", safe=False)
        
            else:
                return JsonResponse("Book not found.", safe=False)
            

def show_authors(request):
    list_author = Author.objects.all().values('id', 'name', 'list_of_books')
    return JsonResponse(list(list_author), safe=False)

def delete_author(request):
    author_id = request.GET.get('id')
    if author_id:
            try:
                int(author_id)
            except ValueError:
                return JsonResponse( "Invalid author ID.", safe=False)
            try:
                author_to_delete = Author.objects.filter(id=author_id)

                if author_to_delete.exists():
                    author_to_delete.delete()
                    return JsonResponse( f"Author with ID {author_id} deleted successfully.", safe=False)
                else:
                    return JsonResponse("author not found.", safe=False)
            except :
                return JsonResponse("error", safe=False)


########################################################
def edit_author(request):
    current_name = request.GET.get('current_name')
    new_name = request.GET.get('new_name')
    
    if not current_name or not new_name:
        return JsonResponse("Please provide both the current name and a new name", safe=False)
    
    if any(not c.isalnum() and c != " " for c in new_name):
        return JsonResponse("Please provide a valid name", safe=False)
    
    try:
        author = Author.objects.get(name=current_name)
    except Author.DoesNotExist:
        return JsonResponse("Author not found", safe=False)
    try:
        existing_author = Author.objects.get (name = new_name)
        author_books = author.list_of_books.split (" , ")
        existing_author_books = existing_author.list_of_books.split(" , ")

        merged_books = list(set(author_books + existing_author_books))
        existing_author.list_of_books = " , ".join(merged_books)
    except Author.DoesNotExist:
        pass

    their_books = Book.objects.filter(author=author.name)
    for book in their_books:
        book.author = new_name
        book.save()
    author.name = new_name
    author.save()
    return JsonResponse("Author updated successfully", safe=False)


# Might go very wrong up if we are removing the last book
def edit_book(request):
    book_id = request.GET.get('book_id')
    new_name = request.GET.get('name')
    new_author_name = request.GET.get('new_author')
    new_price = request.GET.get('price')
    new_edition = request.GET.get('edition')
    new_description = request.GET.get('description')
    
    
    if not book_id:
        return JsonResponse("Please provide a book ID", safe=False)
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse("Book not found", safe=False)
    old_name = book.name
    old_author_name = book.author
    if new_name and new_name != old_name:
        book.name = new_name 
        author = Author.objects.get(name=old_author_name)
        books = [b.strip() for b in author.list_of_books.split(",") if b.strip()]
        updated_books = [new_name if b == old_name else b for b in books]
        author.list_of_books = ", ".join(updated_books)
        author.save()
    else: new_name = book.name

    if new_author_name and new_author_name != old_author_name:
        new_author, created = Author.objects.get_or_create(name=new_author_name)
        old_author = Author.objects.get(name=old_author_name)
        old_books = old_author.list_of_books[:-1].split(",")
        # del old_books[-1]
        old_books.remove(new_name)
        old_author.list_of_books = ",".join(old_books)+","
        print(old_author.list_of_books)
        old_author.save()
        new_author.list_of_books += new_name+","
        new_author.save()
        book.author = new_author_name
    if new_price:
            book.price = float(new_price)
    if new_edition:
        book.edition = new_edition
    if new_description:
        book.description = new_description
    book.save()
    return JsonResponse("Book updated successfully", safe=False)

def sort_alph(request):
    list_book = Book.objects.all().values('id', 'name', 'author', 'price', 'edition', 'description')
    if request.GET.get('order') == "desc":
        sorted_data = sorted(list_book, key=lambda x: x["name"], reverse=True)
    else:
        sorted_data = sorted(list_book, key=lambda x: x["name"])
    return JsonResponse(sorted_data, safe=False)

def sort_price(request):
    list_book = Book.objects.all().values('id', 'name', 'author', 'price', 'edition', 'description')
    if request.GET.get('order') == "desc":
        sorted_data = sorted(list_book, key=lambda x: x["price"], reverse=True)
    else:
        sorted_data = sorted(list_book, key=lambda x: x["price"])
    return JsonResponse(sorted_data, safe=False)

def search_books(request):
    name = request.GET.get('name').lower()
    books = Book.objects.all().values('id', 'name', 'author', 'price', 'edition', 'description')
    exact_books = list(filter(lambda book: book['name'].lower() == name, books))
    query_words = name.split()
    partial_books = list(filter(
        lambda book: all(word in book['name'].lower() for word in query_words) and book['name'].lower() != name,
        books
    ))
    if not (exact_books or partial_books):
        return JsonResponse("Nothing found.", safe=False)
    return JsonResponse((exact_books + partial_books), safe=False)
