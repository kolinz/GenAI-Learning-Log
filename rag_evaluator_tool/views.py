# rag_evaluator_tool/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from .forms import RAGASEvaluationRunForm
from rag_app.models import RAGEvaluation
from rag_config_log.models import RAGConfiguration
from memo_app.models import LearningMemo

class RAGEvaluatorHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'rag_evaluator_tool/evaluator_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "RAGAS評価実行ツールのトップページです。"
        context['api_key_status'] = "未設定"
        return context

evaluator_home = RAGEvaluatorHomeView.as_view()

class RAGASEvaluationRunView(LoginRequiredMixin, View):
    template_name = 'rag_evaluator_tool/ragas_run_form.html'

    def get(self, request, *args, **kwargs):
        form = RAGASEvaluationRunForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RAGASEvaluationRunForm(request.POST)
        if form.is_valid():
            rag_config_instance = form.cleaned_data['rag_config']
            question = form.cleaned_data['question_to_evaluate']
            selected_memos = form.cleaned_data['memos_for_context']

            # --- ここにRAGAS評価のロジックを実装 ---
            # 現時点ではダミー値でログを保存
            faithfulness_score = 0.85
            answer_relevancy_score = 0.92
            context_precision_score = 0.78
            context_recall_score = 0.88
            actual_answer = "（RAGシステムからのダミー回答）"
            ground_truth = "（質問に対する想定回答）"


            evaluation_log = RAGEvaluation.objects.create(
                evaluator=request.user,
                rag_config=rag_config_instance,
                question=question,
                actual_answer=actual_answer,
                ground_truth=ground_truth,
                faithfulness_score=faithfulness_score,
                answer_relevancy_score=answer_relevancy_score,
                context_precision_score=context_precision_score,
                context_recall_score=context_recall_score,
                notes="rag_evaluator_tool から実行された評価ログ（ダミー値）"
            )
            evaluation_log.related_memos_as_context.set(selected_memos)
            evaluation_log.save()

            return redirect(reverse_lazy('rag_app:rag_evaluation_detail', kwargs={'pk': evaluation_log.pk}))
        
        return render(request, self.template_name, {'form': form})

ragas_run_evaluation = RAGASEvaluationRunView.as_view()