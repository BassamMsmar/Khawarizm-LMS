from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from accounts.models import Role
from MainDashboard.forms import StudentForm, UpdateStudentForm
from accounts.decorators import admin_required, staff_required
from django.utils.decorators import method_decorator
import json

User = get_user_model()


@staff_required
def students(request):
    students = User.objects.filter(roles__name__iexact='student')
    student_data = []
    for student in students:
        department = student.department
        college = department.college if department else None

        student_data.append({
            'student': {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'is_active': student.is_active,
                'created_at': student.created_at.isoformat() if student.created_at else None
            },
            'department': {
                'name': department.name if department else None
            },
            'college': {
                'title': college.title if college else None
            }
        })

    return render(request, 'pages/students.html', {'student_data': json.dumps(student_data)})


@admin_required
def toggle_student_status(request, pk):
    student = get_object_or_404(User, pk=pk)
    student.is_active = not student.is_active
    student.save()
    return JsonResponse({'success': True, 'is_active': student.is_active})


@method_decorator(admin_required, name='dispatch')
class StudentCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            # Assign 'student' role
            try:
                student_role = Role.objects.get(name='student')
                student.roles.add(student_role)
            except Role.DoesNotExist:
                # Handle case where 'student' role does not exist
                pass
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(admin_required, name='dispatch')
class StudentUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        student = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(instance=student)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'phone_number': student.phone_number,
                'department': student.department.id if student.department else ''
            }
        })

    def post(self, request, pk, *args, **kwargs):
        student = get_object_or_404(User, pk=pk)
        form = UpdateStudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                student.set_password(password)
            student.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@admin_required
def delete_student(request, pk):
    student = get_object_or_404(User, pk=pk)
    student.delete()
    return redirect('students')
