from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q
from courses.models import Course
from college.models import College
from department.models import Department
from .forms import CourseForm, CollegeForm, DepartmentForm, StudentForm
from django.contrib.auth import get_user_model
from accounts.models import User, Role # Assuming Role model is in accounts.models

User = get_user_model()

# ____________________________________________________________________
from django.shortcuts import render
from courses.models import Course, Lesson  # أو حسب اسم الموديلات عندك
from accounts.models import User  # حسب مكان تعريف User

def dashboard(request):
    courses_count = Course.objects.count()

    students_count = User.objects.filter(roles__name__iexact='student').count()
    lessons_count = Lesson.objects.count()

    context = {
        'courses_count': courses_count,
        'students_count': students_count,
        'lessons_count': lessons_count,
        'certificates_count': 58  # يمكنك تغييره لاحقًا إذا كان ديناميكي
    }

    return render(request, 'pages/dashboard.html', context)


class CollegeListView(ListView):
    model = College
    template_name = 'pages/colleges.html'
    context_object_name = 'colleges'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollegeForm()
        return context


class CollegeCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = CollegeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


class CollegeUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        college = get_object_or_404(College, pk=pk)
        form = CollegeForm(instance=college)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'title': college.title,
                'about': college.about,
                'max_students': college.max_students,
                'is_public': college.is_public,
                'regular_price': str(college.regular_price) if college.regular_price else None,
                'discounted_price': str(college.discounted_price) if college.discounted_price else None,
                'intro_video_url': college.intro_video_url,
                'description': college.description,
                'tags': college.tags,
                'targeted_audience': college.targeted_audience,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        college = get_object_or_404(College, pk=pk)
        form = CollegeForm(request.POST, request.FILES, instance=college)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


def delete_college(request, pk):
    college = College.objects.get(pk=pk)
    college.delete()
    return redirect('/main-dashboard/college/')


def college_search_ajax(request):
    search_query = request.GET.get('q', '')
    colleges = College.objects.all()

    if search_query:
        colleges = colleges.filter(
            Q(title__icontains=search_query)
        ).distinct()

    college_data = []
    for college in colleges:
        college_data.append({
            'id': college.id,
            'slug': college.slug,
            'title': college.title,
            'is_public': college.is_public,
            'max_students': college.max_students,
            'regular_price': str(college.regular_price) if college.regular_price else None,
            'discounted_price': str(college.discounted_price) if college.discounted_price else None,
        })

    return JsonResponse({'colleges': college_data})


# ____________________________________________________________________


class DepartmentListView(ListView):
    model = Department
    template_name = 'pages/departments.html'
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DepartmentForm() # Add DepartmentForm to context
        return context


class DepartmentCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


class DepartmentUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(instance=department)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'name': department.name,
                'college': department.college.id if department.college else '',
                'admin': department.admin.id if department.admin else '',
                'is_active': department.is_active,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('/main-dashboard/departments/')


def department_search_ajax(request):
    search_query = request.GET.get('q', '')
    departments = Department.objects.all()

    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) |
            Q(college__title__icontains=search_query) |
            Q(admin__first_name__icontains=search_query) |
            Q(admin__last_name__icontains=search_query)
        ).distinct()

    department_data = []
    for department in departments:
        department_data.append({
            'id': department.id,
            'slug': department.slug,
            'name': department.name,
            'college': department.college.title if department.college else '',
            'admin': department.admin.get_full_name() if department.admin else '',
            'is_active': department.is_active,
            'created_at': department.created_at.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'departments': department_data})


# ____________________________________________________________________


class CourseListView(ListView):
    model = Course
    template_name = 'pages/courses.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lecturers'] = get_user_model().objects.all()
        context['form'] = CourseForm()

        return context


class CourseCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


class CourseUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(instance=course)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'title': course.title,
                'lecturer': course.lecturer.id if course.lecturer else '',
                'department': course.department.id if course.department else '',
                # أو لو عايز تبعت الاسم كمان
                'department_name': str(course.department) if course.department else '',
                'academic_hours': course.academic_hours,
                'short_description': course.short_description,
                'description': course.description,
                'what_youll_learn': course.what_youll_learn,
                'who_this_course_is_for': course.who_this_course_is_for,
                'is_active': course.is_active,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


def delete_course(request, pk):
    course = Course.objects.get(pk=pk)
    course.delete()
    return redirect('/main-dashboard/courses/')


def course_search_ajax(request):
    search_query = request.GET.get('q', '')
    courses = Course.objects.all()

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(lecturer__first_name__icontains=search_query) |
            Q(lecturer__last_name__icontains=search_query)
        ).distinct()

    course_data = []
    for course in courses:
        course_data.append({
            'id': course.id,
            'slug': course.slug,
            'title': course.title,
            'lecturer_full_name': course.lecturer.get_full_name(),
            'enrolled_count': course.get_enrolled_count(),
            'is_active': course.is_active,
            'created_at': course.created_at.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'courses': course_data})

# ____________________________________________________________________


User = get_user_model()

import json

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


def delete_teacher(request, pk):
    teacher = get_object_or_404(User, pk=pk)
    teacher.delete()
    return redirect('teachers')








# ____________________________________________________________________


User = get_user_model()

import json

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


def toggle_student_status(request, pk):
    student = get_object_or_404(User, pk=pk)
    student.is_active = not student.is_active
    student.save()
    return JsonResponse({'success': True, 'is_active': student.is_active})


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

from .forms import UpdateStudentForm
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


def delete_student(request, pk):
    student = get_object_or_404(User, pk=pk)
    student.delete()
    return redirect('students')

# ____________________________________________________________________


def lessons(request):
    return render(request, 'pages/lessons.html')


# ____________________________________________________________________

def quizzes(request):
    return render(request, 'pages/quizzes.html')


# ____________________________________________________________________


def reports(request):
    return render(request, 'pages/reports.html')


# ____________________________________________________________________


def settings(request):
    return render(request, 'pages/settings.html')

# ____________________________________________________________________
