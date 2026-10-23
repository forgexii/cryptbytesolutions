"""
Cryptbyte Solutions - Home URL Configuration

Maps the root URL route to the primary landing page.
"""

from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
]
