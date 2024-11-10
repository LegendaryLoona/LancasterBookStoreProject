from django.urls import path
from . import views

urlpatterns = [
    path('library/', views.library, name='sample_json_view'),
    path('addauthor/', views.addauthor, name='sample_json_view'),
    path('addbook/', views.addbook, name='sample_json_view'),
]
