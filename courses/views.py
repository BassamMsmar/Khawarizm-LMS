from django.shortcuts import render
from .models import Course, Lesson
from django.views.generic import ListView, DetailView

# Create your views here.



class CourseList(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


# class CourseDetail(DetailView):
#     model = Course
#     template_name = 'course_detail.html'
#     context_object_name = 'course'


from django.views.generic import DetailView
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, Unit

class CourseDetail(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # Get units related to the course
        units = Unit.objects.filter(course=course)

        # Get lessons for each unit
        unit_lessons = {
            unit: unit.lessons.all() for unit in units
        }

        context["related_units"] = units
        context["unit_lessons"] = unit_lessons

        return context

    

class Lesson_Detail(DetailView):
    model = Lesson
    template_name = 'lesson.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'
