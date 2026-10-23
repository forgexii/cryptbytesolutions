"""
Cryptbyte Solutions - Teams URL Configuration

Maps public routes for the staff team directory and individual member profile pages.
"""

from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.team_list, name='teams'),
    path('<int:pk>/', views.team_detail, name='team_detail'),
]
