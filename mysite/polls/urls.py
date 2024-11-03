from django.urls import path
from . import views

urlpatterns = [
    path('finances/', views.finances, name='finances'),
]