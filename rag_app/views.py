# rag_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import RAGEvaluation
from .forms import RAGEvaluationForm
from django.db.models import Q # <-- 検索につかうQオブジェクトをインポート

# --- RAG評価ログ関連ビュー ---

class RAGEvaluationListView(LoginRequiredMixin, ListView):
    model = RAGEvaluation
    template_name = 'rag_app/rag_evaluation_list.html'
    context_object_name = 'evaluations'
    paginate_by = 10

    def get_queryset(self):
        queryset = RAGEvaluation.objects.filter(evaluator=self.request.user).order_by('-evaluation_date')
        query = self.request.GET.get('q') # <-- base.html の検索フォームから送信されたキーワードで、RAG評価ログを横断的に検索

        if query:
            # 複数のフィールドを横断的に検索
            queryset = queryset.filter(
                Q(question__icontains=query) |
                Q(actual_answer__icontains=query) |
                Q(notes__icontains=query)
            )

        return queryset
    
    def get_context_data(self, **kwargs): # <-- base.html の検索フォームから送信されたキーワードで、RAG評価ログを横断的に検索
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

rag_evaluation_list = RAGEvaluationListView.as_view()

class RAGEvaluationDetailView(LoginRequiredMixin, DetailView):
    model = RAGEvaluation
    template_name = 'rag_app/rag_evaluation_detail.html'
    context_object_name = 'evaluation'

rag_evaluation_detail = RAGEvaluationDetailView.as_view()

class RAGEvaluationCreateView(LoginRequiredMixin, CreateView):
    model = RAGEvaluation
    form_class = RAGEvaluationForm
    template_name = 'rag_app/rag_evaluation_form.html'
    success_url = reverse_lazy('rag_app:rag_evaluation_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if not form.instance.evaluator:
            form.instance.evaluator = self.request.user
        return super().form_valid(form)

rag_evaluation_create = RAGEvaluationCreateView.as_view()

class RAGEvaluationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RAGEvaluation
    form_class = RAGEvaluationForm
    template_name = 'rag_app/rag_evaluation_form.html'
    success_url = reverse_lazy('rag_app:rag_evaluation_list')

    def test_func(self):
        evaluation = self.get_object()
        return evaluation.evaluator == self.request.user or self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

rag_evaluation_update = RAGEvaluationUpdateView.as_view()

class RAGEvaluationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RAGEvaluation
    template_name = 'rag_app/rag_evaluation_confirm_delete.html'
    success_url = reverse_lazy('rag_app:rag_evaluation_list')

    def test_func(self):
        evaluation = self.get_object()
        return evaluation.evaluator == self.request.user or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evaluation'] = self.get_object()
        return context

rag_evaluation_delete = RAGEvaluationDeleteView.as_view()