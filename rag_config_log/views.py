# rag_config_log/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import RAGConfiguration
from .forms import RAGConfigurationForm

class RAGConfigurationListView(LoginRequiredMixin, ListView):
    model = RAGConfiguration
    template_name = 'rag_config_log/rag_config_list.html'
    context_object_name = 'configs'
    paginate_by = 10

    def get_queryset(self):
        return RAGConfiguration.objects.filter(user=self.request.user).order_by('-created_at')

rag_config_list = RAGConfigurationListView.as_view()

class RAGConfigurationDetailView(LoginRequiredMixin, DetailView):
    model = RAGConfiguration
    template_name = 'rag_config_log/rag_config_detail.html'
    context_object_name = 'config'

    def test_func(self):
        config = self.get_object()
        return config.user == self.request.user or self.request.user.is_superuser

rag_config_detail = RAGConfigurationDetailView.as_view()

class RAGConfigurationCreateView(LoginRequiredMixin, CreateView):
    model = RAGConfiguration
    form_class = RAGConfigurationForm
    template_name = 'rag_config_log/rag_config_form.html'
    success_url = reverse_lazy('rag_config_log:rag_config_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

rag_config_create = RAGConfigurationCreateView.as_view()

class RAGConfigurationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RAGConfiguration
    form_class = RAGConfigurationForm
    template_name = 'rag_config_log/rag_config_form.html'
    success_url = reverse_lazy('rag_config_log:rag_config_list')

    def test_func(self):
        config = self.get_object()
        return config.user == self.request.user

rag_config_update = RAGConfigurationUpdateView.as_view()

class RAGConfigurationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RAGConfiguration
    template_name = 'rag_config_log/rag_config_confirm_delete.html'
    success_url = reverse_lazy('rag_config_log:rag_config_list')
    context_object_name = 'config'

    def test_func(self):
        config = self.get_object()
        return config.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config'] = self.get_object()
        return context

rag_config_delete = RAGConfigurationDeleteView.as_view()