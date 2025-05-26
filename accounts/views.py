from django.shortcuts import render
from django.views.generic import ListView


from .models import CustomUser


class DashboardView(ListView):
    model = CustomUser
    template_name = 'accounts/dashboard/AdminDashboard/instructorDashboard.html'
    context_object_name = 'users'

# Create your views here.
class UserListView(ListView):
    model = CustomUser
    template_name = 'accounts/dashboard/user_list.html'
    context_object_name = 'users'