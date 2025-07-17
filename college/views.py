from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import College

# Create your views here.


class CollegeList(ListView):
    model = College
    template_name = 'college_list.html'
    context_object_name = 'colleges'


class CollegeDetail(DetailView):
    model = College
    template_name = 'college_detail.html'
    context_object_name = 'college'

class CollegeCreate(CreateView):
    model = College
    template_name = 'college_create.html'
    context_object_name = 'college'
    fields = '__all__'

class CollegeUpdate(UpdateView):
    model = College
    template_name = 'college_update.html'
    context_object_name = 'college'
    fields = '__all__'
class CollegeDelete(DeleteView):
    model = College
    template_name = 'college_delete.html'
    context_object_name = 'college'