# memo_app/admin.py
from django.contrib import admin
from .models import LearningMemo, Tag, MemoAttachment

admin.site.register(LearningMemo)
admin.site.register(Tag)
admin.site.register(MemoAttachment)