# rag_app/forms.py
from django import forms
from .models import RAGEvaluation
from memo_app.models import LearningMemo
from rag_config_log.models import RAGConfiguration

class RAGEvaluationForm(forms.ModelForm):
    rag_config = forms.ModelChoiceField(
        queryset=RAGConfiguration.objects.all().order_by('config_name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="関連RAG構成"
    )

    related_memos_as_context = forms.ModelMultipleChoiceField(
        queryset=LearningMemo.objects.all().order_by('subject', 'year'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="RAGに用いた学習メモ (コンテキスト)"
    )

    class Meta:
        model = RAGEvaluation
        fields = [
            'rag_config',
            'evaluator',
            'evaluation_date',
            'question',
            'related_memos_as_context',
            'ground_truth',
            'actual_answer',
            'faithfulness_score',
            'answer_relevancy_score',
            'context_precision_score',
            'context_recall_score',
            'notes',
        ]
        widgets = {
            'evaluation_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'question': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'ground_truth': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'actual_answer': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'faithfulness_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'min': '0', 'max': '1'}),
            'answer_relevancy_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'min': '0', 'max': '1'}),
            'context_precision_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'min': '0', 'max': '1'}),
            'context_recall_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'min': '0', 'max': '1'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'evaluator': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'rag_config': '関連RAG構成',
            'evaluation_date': '評価日時',
            'evaluator': '評価者',
            'question': '質問文',
            'related_memos_as_context': 'RAGに用いた学習メモ (コンテキスト)',
            'ground_truth': '質問に対する想定回答文',
            'actual_answer': '実際の回答文',
            'faithfulness_score': 'Faithfulness スコア',
            'answer_relevancy_score': 'Answer Relevancy スコア',
            'context_precision_score': 'Context Precision スコア',
            'context_recall_score': 'Context Recall スコア',
            'notes': '備考',
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['related_memos_as_context'].initial = self.instance.related_memos_as_context.all()
            self.fields['rag_config'].initial = self.instance.rag_config
        
        if not self.instance.pk and request and request.user.is_authenticated:
            self.fields['evaluator'].initial = request.user.pk
        
        if self.instance.pk or self.fields['evaluator'].initial:
            self.fields['evaluator'].widget.attrs['disabled'] = 'disabled'
            self.fields['evaluator'].required = False