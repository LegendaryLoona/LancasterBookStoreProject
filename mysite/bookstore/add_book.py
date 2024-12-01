import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
from django.http import JsonResponse
django.setup()
import requests
from bookstore.models import Book,Author
import requests
def add_books(query, total_books=10000, API_KEY="AIzaSyCeEdkjt8iezx-EtUTeeQqnERpgems1UHM"):
    url = "https://www.googleapis.com/books/v1/volumes"
    max_results = 40  
    start_index = 0 
    fetched_books = 0
    while fetched_books < total_books:
        params = {
            "q": query,
            "startIndex": start_index,
            "maxResults": max_results,
            "key": API_KEY
        }
        response = requests.get(url,params=params)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            for item in items:
                volume_info = item.get("volumeInfo", {})
                sale_Info = item.get("saleInfo", {})
                
                title = volume_info.get("title", "")
                authors = volume_info.get("authors", [])  
                description = volume_info.get("description", "")
                edition1 =volume_info.get("edition","")
                listprice = sale_Info.get("listPrice", {}).get("amount", 0)
                book, created = Book.objects.get_or_create(
                    name=title,
                    description= description,
                    price= listprice,
                    edition=edition1
                )
                for authorname in authors:
                    author, author_created = Author.objects.get_or_create(author_name=authorname)
                    book.author.add(author)
                if created:
                    book.save()
            fetched_books += len(items)
            start_index += max_results 
            if len(items) < max_results:
                break 
        else:
            print(f"error，error_code: {response.status_code}")
            print(response.text)

# test command from bookstore.add_book.import add_books
# add_books(query="type")