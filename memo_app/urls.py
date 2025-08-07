# memo_app/urls.py
from django.urls import path
from . import views

app_name = 'memo_app'

urlpatterns = [
    path('', views.memo_list, name='memo_list'),
    path('tag/<str:tag_name>/', views.tagged_memo_list, name='tagged_memo_list'),
    path('new/', views.memo_create, name='memo_create'),
    path('<int:pk>/', views.memo_detail, name='memo_detail'),
    path('<int:pk>/edit/', views.memo_update, name='memo_update'),
    path('<int:pk>/delete/', views.memo_delete, name='memo_delete'),
    path('export/csv/', views.learning_memo_export_csv, name='learning_memo_export_csv'),
]