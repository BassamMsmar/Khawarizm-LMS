from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course

@login_required
def index(request):
    enrolled_courses = request.user.enrolled_courses.all()
    context = {
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'student/index.html', context)

@login_required
def my_courses(request):
    enrolled_courses = request.user.enrolled_courses.all()
    context = {
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'student/my_courses.html', context)

@login_required
def academic_program(request):
    student_department = request.user.department
    department_courses = []
    if student_department:
        department_courses = Course.objects.filter(department=student_department)
    context = {
        'student_department': student_department,
        'department_courses': department_courses
    }
    return render(request, 'student/academic_program.html', context)

@login_required
def my_payments(request):
    return render(request, 'student/my_payments.html')

@login_required
def notifications(request):
    return render(request, 'student/notifications.html')

@login_required
def my_grades(request):
    return render(request, 'student/my_grades.html')

@login_required
def calendar(request):
    return render(request, 'student/calendar.html')

@login_required
def settings(request):
    return render(request, 'student/settings.html')
