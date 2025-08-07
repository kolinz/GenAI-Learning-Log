# rag_evaluator_tool/forms.py
from django import forms
from memo_app.models import LearningMemo
from rag_config_log.models import RAGConfiguration

class RAGASEvaluationRunForm(forms.Form):
    rag_config = forms.ModelChoiceField(
        queryset=RAGConfiguration.objects.all().order_by('config_name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="RAG構成を選択",
        help_text="評価を実行したいRAG構成を選択してください。"
    )

    question_to_evaluate = forms.CharField(
        label="評価する質問文",
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        help_text="RAGシステムに投げかける質問を入力してください。"
    )
    
    memos_for_context = forms.ModelMultipleChoiceField(
        queryset=LearningMemo.objects.all().order_by('subject', 'year'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="コンテキストとして使用する学習メモ",
        help_text="RAGシステムが参照する学習メモを選択してください。"
    )