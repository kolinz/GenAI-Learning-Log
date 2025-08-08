# memo_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Tag(models.Model):
    """メモに付与するタグ"""
    name = models.CharField(max_length=50, unique=True, verbose_name="タグ名")

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"
        ordering = ['name']

    def __str__(self):
        return self.name

# 記録の種類を定義するタプル
RECORD_TYPE_CHOICES = [
    ('memo', '学習メモ'),
    ('conversation', 'AIとの対話記録'),
]

class LearningMemo(models.Model):
    """学習メモを表現するモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作成者")
    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPE_CHOICES,
        default='memo',
        verbose_name="記録の種別"
    )
    input_text = models.TextField(verbose_name="記録内容（マークダウン形式）")
    instruction_text = models.TextField(verbose_name="想定される質問例", blank=True, null=True)
    output_text = models.TextField(verbose_name="質問への回答例", blank=True, null=True)
    subject = models.CharField(max_length=100, verbose_name="科目名")
    unit = models.CharField(max_length=100, blank=True, null=True, verbose_name="単元")
    year = models.IntegerField(verbose_name="年度")
    lesson_date = models.DateField(default=timezone.now, verbose_name="授業日")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="タグ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        ordering = ['-lesson_date', '-created_at']
        verbose_name = "学習メモ"
        verbose_name_plural = "学習メモ"

    def __str__(self):
        return f"{self.subject} - {self.year}年 ({self.lesson_date.strftime('%Y/%m/%d')})"

    def get_absolute_url(self):
        return reverse('memo_app:memo_detail', kwargs={'pk': self.pk})

class MemoAttachment(models.Model):
    """学習メモに添付されるファイル（画像、文書など）"""
    memo = models.ForeignKey(LearningMemo, on_delete=models.CASCADE, related_name='attachments', verbose_name="学習メモ")
    file = models.FileField(upload_to='memo_attachments/', verbose_name="添付ファイル")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="ファイルの説明")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="アップロード日時")

    class Meta:
        verbose_name = "添付ファイル"
        verbose_name_plural = "添付ファイル"
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.file.name.split('/')[-1]} (for {self.memo.subject})"