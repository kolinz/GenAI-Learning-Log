# todo_app/forms.py
from django import forms
from .models import ToDo
from memo_app.models import LearningMemo

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['memo', 'title', 'description', 'due_date', 'is_completed']
        widgets = {
            'memo': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'memo': '関連学習メモ',
            'title': 'タスク名',
            'description': '詳細',
            'due_date': '期限日',
            'is_completed': '完了済み',
        }