from django.urls import path
from . import views

urlpatterns = [
    path('library/', views.library, name='sample_json_view'),
    path('addauthor/', views.addauthor, name='sample_json_view'),
    path('addbook/', views.addbook, name='sample_json_view'),
    path('deletebook/', views.delete_book, name='sample_json_view'),
    path('editauthor/', views.edit_author, name='sample_json_view'),
    path('editbook/', views.edit_book, name='edit_book'),
    path('showauthors/', views.show_authors, name='sample_json_view'),
    path('deleteauthor/', views.delete_author, name='sample_json_view'),
]
