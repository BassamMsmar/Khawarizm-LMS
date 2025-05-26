from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.urls import reverse

from .models import CustomUser

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'student':
            return reverse('dashboard:studentDashboard')
        elif user.user_type == 'lecturer' or user.user_type == 'teaching_assistant':
            return reverse('dashboard:lecturerDashboard')
        elif user.user_type == 'admin'  :
            return reverse('dashboard:adminDashboard')
        else:
            return reverse('home')