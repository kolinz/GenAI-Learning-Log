# rag_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from memo_app.models import LearningMemo
from rag_config_log.models import RAGConfiguration # <-- RAGConfigurationモデルをインポート

class RAGEvaluation(models.Model):
    """
    RAGシステムおよびその評価指標RAGASの評価結果を記録するモデル
    """
    evaluation_date = models.DateTimeField(default=timezone.now, verbose_name="評価日時")
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="評価者")

    rag_config = models.ForeignKey(RAGConfiguration, on_delete=models.CASCADE, verbose_name="RAG構成", related_name='evaluations')

    question = models.TextField(verbose_name="質問文 (RAGAS: question)")
    related_memos_as_context = models.ManyToManyField(LearningMemo, blank=True, verbose_name="RAGに用いた学習メモ (RAGAS: context)")
    ground_truth = models.TextField(blank=True, null=True, verbose_name="質問に対する想定回答文 (RAGAS: ground_truth)")
    actual_answer = models.TextField(verbose_name="実際の回答文 (RAGAS: answer)")

    # RAGAS評価結果 (出力)
    faithfulness_score = models.FloatField(null=True, blank=True, verbose_name="Faithfulness スコア")
    answer_relevancy_score = models.FloatField(null=True, blank=True, verbose_name="Answer Relevancy スコア")
    context_precision_score = models.FloatField(null=True, blank=True, verbose_name="Context Precision スコア")
    context_recall_score = models.FloatField(null=True, blank=True, verbose_name="Context Recall スコア")

    notes = models.TextField(blank=True, null=True, verbose_name="備考（評価プロセスや課題など）")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ログ作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最終更新日時")

    class Meta:
        verbose_name = "RAG評価ログ"
        verbose_name_plural = "RAG評価ログ"
        ordering = ['-evaluation_date']

    def __str__(self):
        return f"評価({self.rag_config.config_name}): {self.question[:50]}... ({self.evaluation_date.strftime('%Y-%m-%d %H:%M')})"

    @property
    def faithfulness_display(self):
        return f"{self.faithfulness_score:.4f}" if self.faithfulness_score is not None else "nan"

    @property
    def answer_relevancy_display(self):
        return f"{self.answer_relevancy_score:.4f}" if self.answer_relevancy_score is not None else "nan"

    @property
    def context_precision_display(self):
        return f"{self.context_precision_score:.4f}" if self.context_precision_score is not None else "nan"

    @property
    def context_recall_display(self):
        return f"{self.context_recall_score:.4f}" if self.context_recall_score is not None else "nan"