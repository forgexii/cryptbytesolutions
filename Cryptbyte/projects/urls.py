"""
Cryptbyte Solutions - Projects URL Configuration

Maps public routes for the projects portfolio catalog and case study detail views.
"""

from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
]
