from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.blog_list, name='blogs'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]

