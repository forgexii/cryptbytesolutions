"""
Cryptbyte Solutions - Dashboard URL Configuration

Maps internal administration endpoints for:
- Authentication (login, logout, session management)
- Overview dashboard KPIs
- Full CRUD workflows for Blogs, Solutions, Projects, Teams, Departments, and Specializations.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Overview & Authentication
    path('', views.dashboard_home, name='home'),
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),

    # Blogs CRUD
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/create/', views.blog_create, name='blog_create'),
    path('blogs/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blogs/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('blogs/<int:pk>/toggle/', views.blog_toggle_publish, name='blog_toggle_publish'),

    # Solutions CRUD
    path('solutions/', views.solution_list, name='solution_list'),
    path('solutions/create/', views.solution_create, name='solution_create'),
    path('solutions/<int:pk>/edit/', views.solution_edit, name='solution_edit'),
    path('solutions/<int:pk>/delete/', views.solution_delete, name='solution_delete'),
    path('solutions/<int:pk>/toggle/', views.solution_toggle_publish, name='solution_toggle_publish'),

    # Projects CRUD
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:pk>/toggle/', views.project_toggle_publish, name='project_toggle_publish'),

    # Teams CRUD
    path('teams/', views.team_list, name='team_list'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('teams/<int:pk>/delete/', views.team_delete, name='team_delete'),

    # Departments & Specializations CRUD
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    path('specializations/create/', views.specialization_create, name='specialization_create'),
    path('specializations/<int:pk>/edit/', views.specialization_edit, name='specialization_edit'),
    path('specializations/<int:pk>/delete/', views.specialization_delete, name='specialization_delete'),
]
