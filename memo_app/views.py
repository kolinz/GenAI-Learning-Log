# memo_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
import csv
import datetime
from .models import LearningMemo, Tag, MemoAttachment
from .forms import LearningMemoForm, MemoAttachmentFormSet
from django.db.models import Q # <-- 検索につかうQオブジェクトをインポート
from todo_app.models import ToDo # <-- ToDo管理モデルをインポート


# --- 検索とフィルタリングの共通ロジック ---
def filter_memos(request, queryset):
    """
    クエリパラメータに基づいて、学習メモのクエリセットをフィルタリングするヘルパー関数。
    """
    record_type = request.GET.get('record_type')
    query = request.GET.get('q')

    if record_type:
        queryset = queryset.filter(record_type=record_type)

    if query:
        queryset = queryset.filter(
            Q(input_text__icontains=query) |
            Q(subject__icontains=query)
        )
    return queryset

# --- 学習メモ関連ビュー ---

class MemoListView(LoginRequiredMixin, ListView):
    model = LearningMemo
    template_name = 'memo_app/memo_list.html'
    context_object_name = 'memos'
    paginate_by = 9
    
    def get_queryset(self):
        # まずログインユーザーのメモを取得し、その後にヘルパー関数でフィルタリングする
        queryset = LearningMemo.objects.filter(user=self.request.user).order_by('-created_at')
        return filter_memos(self.request, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_record_type'] = self.request.GET.get('record_type')
        context['query'] = self.request.GET.get('q', '') # <-- 検索フォームへの値の再設定 /memos/?q=キーワード のようになる
        return context

memo_list = MemoListView.as_view()

class MemoDetailView(LoginRequiredMixin, DetailView):
    model = LearningMemo
    template_name = 'memo_app/memo_detail.html'
    context_object_name = 'memo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        memo = self.get_object()
        context['todos'] = memo.todos.all() # <-- 関連付けられたToDoリストを取得
        return context

memo_detail = MemoDetailView.as_view()

class MemoCreateView(LoginRequiredMixin, CreateView):
    model = LearningMemo
    form_class = LearningMemoForm
    template_name = 'memo_app/memo_form.html'
    success_url = reverse_lazy('memo_app:memo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attachment_formset'] = MemoAttachmentFormSet(self.request.POST, self.request.FILES)
        else:
            context['attachment_formset'] = MemoAttachmentFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attachment_formset = context['attachment_formset']

        if form.is_valid() and attachment_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            form.save_m2m()

            attachment_formset.instance = self.object
            attachment_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

memo_create = MemoCreateView.as_view()

class MemoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LearningMemo
    form_class = LearningMemoForm
    template_name = 'memo_app/memo_form.html'
    success_url = reverse_lazy('memo_app:memo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attachment_formset'] = MemoAttachmentFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['attachment_formset'] = MemoAttachmentFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        attachment_formset = context['attachment_formset']

        if form.is_valid() and attachment_formset.is_valid():
            self.object = form.save()
            attachment_formset.instance = self.object
            attachment_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def test_func(self):
        memo = self.get_object()
        return memo.user == self.request.user

memo_update = MemoUpdateView.as_view()

class MemoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LearningMemo
    template_name = 'memo_app/memo_confirm_delete.html'
    success_url = reverse_lazy('memo_app:memo_list')
    context_object_name = 'memo'

    def test_func(self):
        memo = self.get_object()
        return memo.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memo'] = self.get_object()
        return context

memo_delete = MemoDeleteView.as_view()

class TaggedMemoListView(LoginRequiredMixin, ListView):
    model = LearningMemo
    template_name = 'memo_app/memo_list.html'
    context_object_name = 'memos'
    paginate_by = 9

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return LearningMemo.objects.filter(
            user=self.request.user,
            tags__name=tag_name
        ).order_by('-created_at').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_tag'] = self.kwargs['tag_name']
        return context

tagged_memo_list = TaggedMemoListView.as_view()


# --- CSVエクスポートビュー ---
class LearningMemoExportCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # GETリクエストの場合の処理 (全メモをエクスポート)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="learning_memos.csv"'
        
        writer = csv.writer(response)
        
        writer.writerow([
            'ID', '作成者', '記録の種別', '記録内容', '科目名', '年度', '単元', '授業日', '想定される質問例',
            '質問への回答例', 'タグ', '作成日時', '更新日時'
        ])

        memos = LearningMemo.objects.filter(user=request.user).order_by('created_at')

        for memo in memos:
            tags = ", ".join([tag.name for tag in memo.tags.all()])
            writer.writerow([
                memo.id, memo.user.username, memo.get_record_type_display(), memo.input_text,
                memo.subject, memo.year, memo.unit, 
                memo.lesson_date.strftime('%Y-%m-%d'),
                memo.instruction_text, memo.output_text, tags,
                memo.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                memo.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        return response

    def post(self, request, *args, **kwargs):
        # POSTリクエストの場合の処理 (選択されたメモのIDでフィルタリング)
        selected_memos_ids = request.POST.getlist('selected_memos')
        if not selected_memos_ids:
            return redirect('memo_app:memo_list')

        # フォームから選択されたフィールドを取得
        selected_fields = request.POST.getlist('fields')
        if not selected_fields:
            # フィールドが選択されていない場合は、すべての項目を出力
            selected_fields = [
                'id', 'user__username', 'get_record_type_display', 'input_text',
                'subject', 'year', 'unit', 'lesson_date',
                'instruction_text', 'output_text', 'tags_list',
                'created_at', 'updated_at'
            ]

        # 出力するフィールドのヘッダーを生成
        header_map = {
            'id': 'ID',
            'user__username': '作成者',
            'get_record_type_display': '記録の種別',
            'input_text': '記録内容',
            'subject': '科目名',
            'year': '年度',
            'unit': '単元',
            'lesson_date': '授業日',
            'instruction_text': '想定される質問例',
            'output_text': '質問への回答例',
            'tags_list': 'タグ',
            'created_at': '作成日時',
            'updated_at': '更新日時',
        }
        headers = [header_map.get(field, field) for field in selected_fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="selected_memos.csv"'

        writer = csv.writer(response)
        writer.writerow(headers)

        memos = LearningMemo.objects.filter(user=request.user, id__in=selected_memos_ids).order_by('created_at')

        for memo in memos:
            row = []
            for field in selected_fields:
                if field == 'tags_list':
                    value = ", ".join([tag.name for tag in memo.tags.all()])
                elif field == 'user__username':
                    value = memo.user.username
                elif field == 'get_record_type_display':
                    value = memo.get_record_type_display()
                else:
                    value = getattr(memo, field)
                
                # 日付型の場合、文字列にフォーマット
                # lesson_dateには時間を含めず、created_atとupdated_atには時間を含めるように修正
                if isinstance(value, datetime.date):
                    value = value.strftime('%Y-%m-%d')
                elif isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')

                row.append(value)
            writer.writerow(row)
            
        return response

learning_memo_export_csv = LearningMemoExportCSVView.as_view()