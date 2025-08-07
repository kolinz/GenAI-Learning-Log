# rag_app/urls.py
from django.urls import path
from . import views

app_name = 'rag_app'

urlpatterns = [
    path('', views.rag_evaluation_list, name='rag_evaluation_list'),
    path('new/', views.rag_evaluation_create, name='rag_evaluation_create'),
    path('<int:pk>/', views.rag_evaluation_detail, name='rag_evaluation_detail'),
    path('<int:pk>/edit/', views.rag_evaluation_update, name='rag_evaluation_update'),
    path('<int:pk>/delete/', views.rag_evaluation_delete, name='rag_evaluation_delete'),
]