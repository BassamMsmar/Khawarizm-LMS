from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy

from .models import CustomUser

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'student':
            return reverse('dashboard:student:studentDashboard')
        elif user.user_type == 'lecturer' or user.user_type == 'teaching_assistant':
            return reverse('dashboard:lecturer:lecturerDashboard')
        elif user.user_type == 'admin'  :
            return reverse('dashboard:admin:adminDashboard')
        else:
            return reverse('home')


class UserLogoutView(LogoutView):
    def get_next_page(self):
        return reverse_lazy('accounts:login')
