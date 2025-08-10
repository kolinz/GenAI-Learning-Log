# config/views.py

from django.shortcuts import render
from django.db.models import Q
from memo_app.models import LearningMemo
from rag_app.models import RAGEvaluation
from rag_config_log.models import RAGConfiguration
from todo_app.models import ToDo

def search_results_view(request):
    """
    ToDoモデル以外を横断的に検索するビュー
    """
    query = request.GET.get('q')
    results = {
        'memos': [],
        'rag_configs': [],
        'rag_evals': [],
        'todos': []
    }

    if query:
        # 学習メモを検索
        memo_queryset = LearningMemo.objects.filter(
            Q(input_text__icontains=query) | Q(subject__icontains=query)
        ).order_by('-created_at')
        results['memos'] = memo_queryset

        # RAG構成を検索
        rag_config_queryset = RAGConfiguration.objects.filter(
            Q(config_name__icontains=query) | Q(description__icontains=query)
        ).order_by('-created_at')
        results['rag_configs'] = rag_config_queryset

        # RAG評価ログを検索
        rag_eval_queryset = RAGEvaluation.objects.filter(
            Q(question__icontains=query) | Q(actual_answer__icontains=query) | Q(notes__icontains=query)
        ).order_by('-evaluation_date')
        results['rag_evals'] = rag_eval_queryset

        # ToDoを検索
        todo_queryset = ToDo.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by('-created_at')
        results['todos'] = todo_queryset


    context = {'query': query, 'results': results}
    return render(request, 'search_results.html', context)