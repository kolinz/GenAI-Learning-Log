# rag_config_log/forms.py (最終修正版)
from django import forms
from .models import RAGConfiguration, RAG_TYPE_CHOICES
from memo_app.models import LearningMemo

class RAGConfigurationForm(forms.ModelForm):
    used_memos = forms.ModelMultipleChoiceField(
        queryset=LearningMemo.objects.all().order_by('subject', 'year'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), # Bootstrapのチェックボックス用クラスを指定
        required=False,
        label="使用した学習メモ"
    )

    class Meta:
        model = RAGConfiguration
        fields = [
            'config_name',
            'rag_model_name',
            'rag_model_version',
            'embedding_model_name',
            'embedding_model_version',
            'rag_tool_name',
            'rag_tool_version',
            'rag_type',
            'rag_workflow_file',
            'description',
            'used_memos',
        ]
        # widgetsで全てのフィールドにクラスを明示的に指定
        widgets = {
            'config_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rag_model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rag_model_version': forms.TextInput(attrs={'class': 'form-control'}),
            'embedding_model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'embedding_model_version': forms.TextInput(attrs={'class': 'form-control'}),
            'rag_tool_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rag_tool_version': forms.TextInput(attrs={'class': 'form-control'}),
            'rag_type': forms.Select(attrs={'class': 'form-select'}),
            'rag_workflow_file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
        labels = {
            'config_name': 'RAG構成名',
            'rag_model_name': 'RAGに使ったLLM',
            'rag_model_version': 'RAGに使ったLLMバージョン',
            'embedding_model_name': 'RAGに使ったEmbeddingモデル',
            'embedding_model_version': 'Embeddingモデルバージョン',
            'rag_tool_name': 'RAGツール名 (例: LlamaIndex, LangChain, Difyなど)',
            'rag_tool_version': 'RAGツールバージョン',
            'rag_type': 'RAGの種類',
            'rag_workflow_file': 'ワークフローファイル',
            'description': 'RAG構成の詳細説明',
            'used_memos': '使用した学習メモ',
        }
    
    def __init__(self, *args, **kwargs):
        # used_memos の初期値を設定するロジックだけを残す
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['used_memos'].initial = self.instance.used_memos.all()