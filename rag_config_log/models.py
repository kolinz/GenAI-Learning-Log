# rag_config_log/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from memo_app.models import LearningMemo

# RAGの種類を定義するタプル
RAG_TYPE_CHOICES = [
    ('Standard', 'Standard RAG (Retrieval-Augmented Generation)'),
    ('Graph', 'GraphRAG'),
    ('HyDE', 'HyDE (Hypothetical Document Embeddings)'),
    ('Multi-hop', 'Multi-hop RAG'),
    ('Fusion', 'Fusion RAG (e.g., RRF)'),
    ('Agentic', 'Agentic RAG'),
    ('Other', 'その他'),
    ('none', 'RAG未使用'),
]

class RAGConfiguration(models.Model):
    """
    RAG（AIエージェント）システムの構成情報（ビルドログ）を記録するモデル
    """
    config_name = models.CharField(max_length=200, unique=True, verbose_name="AIエージェント構成名 (ユニークな識別子)")
    rag_model_name = models.CharField(max_length=200, verbose_name="LLM名")
    rag_model_version = models.CharField(max_length=100, blank=True, null=True, verbose_name="LLMバージョン")
    embedding_model_name = models.CharField(max_length=200, verbose_name="Embeddingモデル")
    embedding_model_version = models.CharField(max_length=100, blank=True, null=True, verbose_name="Embeddingモデルバージョン")
    rag_tool_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="ツール名 (例: Dify, Langflow)")
    rag_tool_version = models.CharField(max_length=100, blank=True, null=True, verbose_name="ツールバージョン")
    rag_type = models.CharField(
        max_length=50,
        choices=RAG_TYPE_CHOICES,
        default='Standard',
        verbose_name="RAGの種類"
    )

    rag_workflow_file = models.FileField(upload_to='rag_workflows/', blank=True, null=True, verbose_name="ワークフローファイル (.json, .yamlなど)")

    used_memos = models.ManyToManyField(
        LearningMemo,
        blank=True,
        related_name='rag_configs',
        verbose_name="使用した学習メモ"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作成者")
    description = models.TextField(blank=True, null=True, verbose_name="AIエージェント構成の詳細説明")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最終更新日時")

    class Meta:
        verbose_name = "AIエージェント構成ログ"
        verbose_name_plural = "AIエージェント構成ログ"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.config_name} ({self.rag_model_name}, {self.rag_type})"