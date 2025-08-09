# todo_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import ToDo
from .forms import ToDoForm

class ToDoListView(LoginRequiredMixin, ListView):
    model = ToDo
    template_name = 'todo_app/todo_list.html'
    context_object_name = 'todos'
    paginate_by = 10

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user).order_by('-created_at')

todo_list = ToDoListView.as_view()

class ToDoDetailView(LoginRequiredMixin, DetailView):
    model = ToDo
    template_name = 'todo_app/todo_detail.html'
    context_object_name = 'todo'

todo_detail = ToDoDetailView.as_view()

class ToDoCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    form_class = ToDoForm
    template_name = 'todo_app/todo_form.html'
    success_url = reverse_lazy('todo_app:todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

todo_create = ToDoCreateView.as_view()

class ToDoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ToDo
    form_class = ToDoForm
    template_name = 'todo_app/todo_form.html'
    success_url = reverse_lazy('todo_app:todo_list')

    def test_func(self):
        todo = self.get_object()
        return todo.user == self.request.user

todo_update = ToDoUpdateView.as_view()

class ToDoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ToDo
    template_name = 'todo_app/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_app:todo_list')

    def test_func(self):
        todo = self.get_object()
        return todo.user == self.request.user

todo_delete = ToDoDeleteView.as_view()