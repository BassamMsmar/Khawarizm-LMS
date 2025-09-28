from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import College
from courses.models import Course
from accounts.models import User
from department.models import Department

# Create your views here.


class CollegeList(ListView):
    model = College
    template_name = 'college_list.html'
    context_object_name = 'colleges'


class CollegeDetail(DetailView):
    model = College
    template_name = 'college_detail.html'
    context_object_name = 'college'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        college = self.get_object()
        
        context['num_departments'] = college.departments.count()
        context['num_courses'] = Course.objects.filter(department__college=college).count()
        context['num_teachers'] = User.objects.filter(department__college=college, profile_type='lecturer').count()
        context['num_students'] = User.objects.filter(department__college=college, profile_type='student').count()
        
        return context

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

class CollegeDepartmentList(ListView):
    model = Department
    template_name = 'college_department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        self.college = get_object_or_404(College, slug=self.kwargs['slug'])
        return Department.objects.filter(college=self.college)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college'] = self.college
        return context

class CollegeCourseList(ListView):
    model = Course
    template_name = 'college_course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        self.college = get_object_or_404(College, slug=self.kwargs['slug'])
        return Course.objects.filter(department__college=self.college)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college'] = self.college
        return context

class CollegeTeacherList(ListView):
    model = User
    template_name = 'college_teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        self.college = get_object_or_404(College, slug=self.kwargs['slug'])
        return User.objects.filter(department__college=self.college, profile_type='lecturer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college'] = self.college
        return context

class CollegeStudentList(ListView):
    model = User
    template_name = 'college_student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        self.college = get_object_or_404(College, slug=self.kwargs['slug'])
        return User.objects.filter(department__college=self.college, profile_type='student')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college'] = self.college
        return context
