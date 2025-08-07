# rag_config_log/admin.py
from django.contrib import admin
from .models import RAGConfiguration

admin.site.register(RAGConfiguration)