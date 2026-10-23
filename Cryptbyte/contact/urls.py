"""
Cryptbyte Solutions - Contact URL Configuration

Maps public routes for the communication hub, location coordinates, and project enquiry form.
"""

from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
]
