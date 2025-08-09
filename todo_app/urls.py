# todo_app/urls.py
from django.urls import path
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('new/', views.todo_create, name='todo_create'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
    path('<int:pk>/edit/', views.todo_update, name='todo_update'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
]