# memo_app/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import LearningMemo, Tag, MemoAttachment, RECORD_TYPE_CHOICES

class LearningMemoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="タグ"
    )

    record_type = forms.ChoiceField(
        choices=RECORD_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="記録の種別"
    )

    class Meta:
        model = LearningMemo
        fields = ['subject', 'unit', 'year', 'lesson_date', 'input_text', 'record_type' , 'instruction_text', 'output_text', 'tags']
        widgets = {
            'record_type': forms.Select(attrs={'class': 'form-select'}),
            'input_text': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'instruction_text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'output_text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'lesson_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'record_type': '記録の種別',
            'input_text': '記録内容（マークダウン形式）',
            'instruction_text': '想定される質問例',
            'output_text': '質問への回答例',
            'subject': '科目名',
            'unit': '単元',
            'year': '年度',
            'lesson_date': '授業日',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = self.instance.tags.all()

MemoAttachmentFormSet = inlineformset_factory(
    LearningMemo,
    MemoAttachment,
    fields=('file', 'description'),
    extra=1,
    can_delete=True,
    widgets={
        'file': forms.FileInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
    }
)