from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from accounts.models import Role
from MainDashboard.forms import StudentForm, UpdateStudentForm
from accounts.decorators import admin_required
from django.utils.decorators import method_decorator
import json
from courses.models import Course

User = get_user_model()


@admin_required
def teachers(request):
    teachers = User.objects.filter(roles__name__iexact='lecturer')
    teacher_data = []
    for teacher in teachers:
        department = teacher.department
        college = department.college if department else None

        teacher_data.append({
            'teacher': {
                'id': teacher.id,
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'email': teacher.email,
                'created_at': teacher.created_at.isoformat() if teacher.created_at else None
            },
            'department': {
                'name': department.name if department else None
            },
            'college': {
                'title': college.title if college else None
            }
        })

    return render(request, 'pages/teachers.html', {'teacher_data': json.dumps(teacher_data)})


@method_decorator(admin_required, name='dispatch')
class TeacherCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.save()
            # Assign 'lecturer' role
            try:
                teacher_role = Role.objects.get(name='lecturer')
                teacher.roles.add(teacher_role)
            except Role.DoesNotExist:
                # Handle case where 'lecturer' role does not exist
                pass
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(admin_required, name='dispatch')
class TeacherUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(instance=teacher)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'email': teacher.email,
                'phone_number': teacher.phone_number,
                'department': teacher.department.id if teacher.department else ''
            }
        })

    def post(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(request.POST, instance=teacher)
        if form.is_valid():
            teacher = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                teacher.set_password(password)
            teacher.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@admin_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    teacher.delete()
    return redirect('teachers')


class TeacherDetail(DetailView):
    model = User
    template_name = 'pages/teacher_detail.html'
    context_object_name = 'teacher'

    def get_queryset(self):
        return super().get_queryset().filter(roles__name__iexact='lecturer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.get_object()
        context['courses_taught'] = Course.objects.filter(lecturer=teacher)
        return context

def teacher_profile(request, pk):
    teacher = get_object_or_404(User, pk=pk, roles__name__iexact='lecturer')

    if not request.user.is_staff and request.user != teacher:
        return redirect('dashboard') # Or some other appropriate redirect/error
    courses_taught = Course.objects.filter(lecturer=teacher)
    
    context = {
        'teacher': teacher,
        'courses_taught': courses_taught,
    }
    return render(request, 'main/teacher_profile.html', context)


def teacher_id_card(request, pk):
    teacher = get_object_or_404(User, pk=pk, roles__name__iexact='lecturer')

    if not request.user.is_staff and request.user != teacher:
        return redirect('dashboard') # Or some other appropriate redirect/error

    context = {
        'teacher': teacher,
    }
    return render(request, 'main/teacher_id_card.html', context)
