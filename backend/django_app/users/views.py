from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, get_object_or_404

class UserMixin(CreateView):
    model = User
    form_class = UserForm
    template_name = 'User/User.html'
    success_url = reverse_lazy('User:list')
    
class UserCreateView(UserMixin, CreateView):
    pass

class UserListView(ListView):
    model = User
    ordering = 'id'
    paginate_by = 10

class UserUpdateView(UserMixin, UpdateView):
    pass

class UserDeleteView(DeleteView):
    model = User
    template_name = 'User/User.html'
    success_url = reverse_lazy('User:list')
