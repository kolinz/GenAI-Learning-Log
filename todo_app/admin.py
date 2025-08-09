# todo_app/admin.py
from django.contrib import admin
from .models import ToDo

admin.site.register(ToDo)