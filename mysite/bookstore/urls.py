from django.urls import path
from . import views

urlpatterns = [
    path('addauthor/', views.addauthor, name='sample_json_view'),
    path('addbook/', views.addbook, name='sample_json_view'),
    path('delete_book/', views.delete_book, name='delete_book'),
    path('search_book/', views.search_book, name='search_book'),
    path('delete_author/', views.delete_author, name='delete_author'),
    path('search_author/', views.search_author, name='search_author'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('edit_author/', views.edit_author, name='edit_author'),
    path('sortalph/', views.sort_alph, name='sample_json_view'),
    path('sortprice/', views.sort_price, name='sample_json_view'),
    ]
