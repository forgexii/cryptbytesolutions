from django.urls import path
from . import views

app_name = 'solutions'

urlpatterns = [
    path('', views.solutions, name='solutions'),
    path('<slug:slug>/', views.solution_detail, name='detail'),
]
