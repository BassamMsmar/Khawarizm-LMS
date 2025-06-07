from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy

from .models import User

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'


class UserLogoutView(LogoutView):
    def get_next_page(self):
        return reverse_lazy('accounts:login')
