from django.urls import path
from . import views

urlpatterns = [
    path('library/', views.library, name='sample_json_view'),
]