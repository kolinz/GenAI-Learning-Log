from django.db import models

# Create your models here.
# todo_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from memo_app.models import LearningMemo

class ToDo(models.Model):
    """学習メモに関連付けられるToDoタスク"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作成者")
    memo = models.ForeignKey(LearningMemo, on_delete=models.CASCADE, related_name='todos', verbose_name="関連学習メモ")
    title = models.CharField(max_length=255, verbose_name="タスク名")
    description = models.TextField(verbose_name="詳細", blank=True, null=True)
    due_date = models.DateTimeField(verbose_name="期限日", blank=True, null=True)
    is_completed = models.BooleanField(default=False, verbose_name="完了済み")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    class Meta:
        verbose_name = "ToDo"
        verbose_name_plural = "ToDo"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title