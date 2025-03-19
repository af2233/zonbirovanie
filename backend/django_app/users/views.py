from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from users.models import User


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
