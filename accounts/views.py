from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy

from .models import User

class UserLoginView(LoginView):
    template_name = 'accounts/new_login.html'


class UserLogoutView(LogoutView):
    def get_next_page(self):
        return reverse_lazy('accounts:login')

def redirect_user(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.has_role('staff') or request.user.has_role('admin'):
            # Redirect to the main dashboard
            return redirect('/main-dashboard/dashboard')
        elif request.user.has_role('student'):
            return redirect('student:index')
        else:
            # Handle other roles or users with no roles
            return redirect('/') # Or a default page
    else:
        return redirect('accounts:login')

# accounts/views.py
from django.shortcuts import render

def unauthorized_view(request):
    return render(request, 'accounts/unauthorized.html', status=403)
