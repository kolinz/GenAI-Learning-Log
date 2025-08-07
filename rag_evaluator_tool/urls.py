# rag_evaluator_tool/urls.py
from django.urls import path
from . import views

app_name = 'rag_evaluator_tool'

urlpatterns = [
    path('', views.evaluator_home, name='evaluator_home'),
    path('run/', views.ragas_run_evaluation, name='run_evaluation'),
]