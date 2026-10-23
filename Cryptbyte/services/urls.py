"""
Cryptbyte Solutions - Services URL Configuration

Maps public routes for the technical consulting and engineering services catalog.
"""

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services, name='services'),
]
