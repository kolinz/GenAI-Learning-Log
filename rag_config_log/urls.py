# rag_config_log/urls.py
from django.urls import path
from . import views

app_name = 'rag_config_log'

urlpatterns = [
    path('', views.rag_config_list, name='rag_config_list'),
    path('new/', views.rag_config_create, name='rag_config_create'),
    path('<int:pk>/', views.rag_config_detail, name='rag_config_detail'),
    path('<int:pk>/edit/', views.rag_config_update, name='rag_config_update'),
    path('<int:pk>/delete/', views.rag_config_delete, name='rag_config_delete'),
]