"""
Cryptbyte Solutions - About URL Configuration

Maps public routes for firm background, engineering philosophy, and organizational statistics.
"""

from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.about, name='about'),
]
