# memo_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
import csv
from .models import LearningMemo, Tag, MemoAttachment
from .forms import LearningMemoForm, MemoAttachmentFormSet


# --- 学習メモ関連ビュー ---

class MemoListView(LoginRequiredMixin, ListView):
    model = LearningMemo
    template_name = 'memo_app/memo_list.html'
    context_object_name = 'memos'
    paginate_by = 9

    def get_queryset(self):
        return LearningMemo.objects.filter(user=self.request.user).order_by('-created_at')

memo_list = MemoListView.as_view()

class MemoDetailView(LoginRequiredMixin, DetailView):
    model = LearningMemo
    template_name = 'memo_app/memo_detail.html'
    context_object_name = 'memo'

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

tagged_memo_list = TaggedMemoListView.as_view


class LearningMemoExportCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="learning_memos.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'ID', '作成者', '科目名', '年度', '授業日', '学習したこと', '想定される質問例',
            '質問への回答例', 'タグ', '作成日時', '更新日時'
        ])

        memos = LearningMemo.objects.filter(user=request.user).order_by('created_at')

        for memo in memos:
            tags = ", ".join([tag.name for tag in memo.tags.all()])

            writer.writerow([
                memo.id,
                memo.user.username,
                memo.subject,
                memo.year,
                memo.lesson_date.strftime('%Y-%m-%d'),
                memo.input_text,
                memo.instruction_text,
                memo.output_text,
                tags,
                memo.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                memo.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        return response

learning_memo_export_csv = LearningMemoExportCSVView.as_view()