from django.shortcuts import render
from django.views.generic import ListView


from .models import CustomUser



# Create your views here.
class UserListView(ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'