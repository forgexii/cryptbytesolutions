"""
Cryptbyte Solutions - Solutions URL Configuration

Maps public routes for the solutions catalog and individual architectural detail pages.
"""

from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    path('', views.solutions, name='solutions'),
    path('<slug:slug>/', views.solution_detail, name='solution_detail'),
    path('<slug:slug>/', views.solution_detail, name='detail'),  # Backwards compatibility alias
]
