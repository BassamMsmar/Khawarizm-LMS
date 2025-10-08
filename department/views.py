from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Department
from courses.models import Course

class DepartmentList(ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'

class DepartmentDetail(DetailView):
    model = Department
    template_name = 'department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context['courses'] = Course.objects.filter(department=department)
        return context

class DepartmentCreate(CreateView):
    model = Department
    template_name = 'department_form.html'
    fields = '__all__'

class DepartmentUpdate(UpdateView):
    model = Department
    template_name = 'department_form.html'
    fields = '__all__'

class DepartmentDelete(DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = '/' # Redirect to a proper URL after deletion
