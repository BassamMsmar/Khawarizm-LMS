from django.shortcuts import render
from .models import Course
from django.views.generic import ListView, DetailView

# Create your views here.



class CourseList(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


class CourseDetail(DetailView):
    model = Course
    template_name = 'courseDetails.html'
    context_object_name = 'course'
