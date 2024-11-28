from .models import Book, Author
from django.http import JsonResponse
from django.db.models import Q,Prefetch
import requests
import threading
from queue import Queue

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
    if new_name:
        book.name = new_name
    if new_price:
        try:
            float(new_price)
        except:
            return JsonResponse("Please provide a valid price", safe=False)
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
    list_book = Book.objects.all().prefetch_related(Prefetch('author', to_attr='authors_list'))
    data = []
    for book in list_book:
        data.append({'id': book.id,'name': book.name,'authors': [author.author_name for author in book.authors_list], 'price': book.price,'edition': book.edition,'description': book.description,})
    if request.GET.get('order') == "desc":
        sorted_data = sorted(data, key=lambda x: x["name"], reverse=True)
    else:
        sorted_data = sorted(data, key=lambda x: x["name"])
    return JsonResponse(sorted_data, safe=False)

def sort_price(request):
    list_book = Book.objects.all().prefetch_related(Prefetch('author', to_attr='authors_list'))
    data = []
    for book in list_book:
        data.append({'id': book.id,'name': book.name,'authors': [author.author_name for author in book.authors_list], 'price': book.price,'edition': book.edition,'description': book.description,})
    if request.GET.get('order') == "desc":
        sorted_data = sorted(data, key=lambda x: x["price"], reverse=True)
    else:
        sorted_data = sorted(data, key=lambda x: x["price"])
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
    books = Book.objects.filter(query).prefetch_related(Prefetch('author', to_attr='authors_list'))
    if not books.exists():
        return JsonResponse("Book not found.", safe=False)
    data = []
    for book in books:
        data.append({'id': book.id,'name': book.name,'authors': [author.author_name for author in book.authors_list], 'price': book.price,'edition': book.edition,'description': book.description,})
    return JsonResponse(data, safe=False)

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
    if not results.exists():
        return JsonResponse("author not found.", safe=False)
    response_data = []
    for author in results:
        response_data.append({
            "author_id" :author.id,
            'author_name': author.author_name,
            'books': author.list_of_books() 
        })
    return JsonResponse(response_data, safe=False)    

def add_books(request):
    if request.method == "GET":
        query_list = request.GET.getlist("query")  
        total_books = int(request.GET.get("total_books", 10000))  
        api_key = request.GET.get("api_key", "AIzaSyCeEdkjt8iezx-EtUTeeQqnERpgems1UHM") 
        max_threads = int(request.GET.get("max_threads", 5)) 
        if not query_list:
            return JsonResponse("error lack of query",safe=False)
        task_queue = Queue()
        for query in query_list:
            task_queue.put(query) 
        def worker():
            while not task_queue.empty():
                query = task_queue.get()  
                if query is None:
                    break 
                url = "https://www.googleapis.com/books/v1/volumes"
                max_results = 40  
                start_index = 0
                fetched_books = 0
                while fetched_books < total_books:
                    remaining_books = total_books - fetched_books
                    current_max_results = min(max_results, remaining_books)  
                    params = {
                        "q": query,
                        "startIndex": start_index,
                        "maxResults": current_max_results, 
                        "key": api_key,
                    }
                    try:
                        response = requests.get(url, params=params)
                        if response.status_code == 200:
                            data = response.json()
                            items = data.get("items", [])
                            for item in items:
                                volume_info = item.get("volumeInfo", {})
                                sale_info = item.get("saleInfo", {})
                                title = volume_info.get("title", "")
                                authors = volume_info.get("authors", [])
                                description = volume_info.get("description", "")
                                edition = volume_info.get("edition", "")
                                list_price = sale_info.get("listPrice", {}).get("amount", 0)
                                book, created = Book.objects.get_or_create(
                                    name=title,
                                    description=description,
                                    price=list_price,
                                    edition=edition,
                                )
                                for author_name in authors:
                                    author, _ = Author.objects.get_or_create(author_name=author_name)
                                    book.author.add(author)
                                if created:
                                    book.save()
                            fetched_books += len(items)
                            start_index += current_max_results
                            if len(items) < current_max_results:
                                break  
                        else:
                            print(f"failed,status: {response.status_code}, error_information: {response.text}")
                            break
                    except Exception as e:
                        print(f"error: {e}")
                        break
                task_queue.task_done()
        threads = []
        for _ in range(min(max_threads, task_queue.qsize())):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        task_queue.join()  
        for thread in threads:
            thread.join() 
        return JsonResponse("successful add book",safe=False)
    return JsonResponse( "noly support GET request",safe=False)
