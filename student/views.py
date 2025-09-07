from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Unit
from .models import Student, Payment
from .forms import PaymentForm
from django.db.models import Sum

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
    courses_with_progress = []
    for course in enrolled_courses:
        total_lessons = course.lessons.count()
        completed_lessons_count = course.lessons.filter(completed_by=request.user).count()
        progress = (completed_lessons_count / total_lessons) * 100 if total_lessons > 0 else 0
        
        units = []
        for unit in course.units.all():
            lessons = []
            for lesson in unit.lessons.all():
                is_completed = lesson.completed_by.filter(id=request.user.id).exists()
                lessons.append({
                    'lesson': lesson,
                    'is_completed': is_completed,
                })
            units.append({
                'unit': unit,
                'lessons': lessons,
            })

        courses_with_progress.append({
            'course': course,
            'progress': progress,
            'units': units,
        })

    context = {
        'courses_with_progress': courses_with_progress
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
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = student
            payment.save()
            return redirect('student:payment_history')
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'student/my_payments.html', context)

@login_required
def payment_history(request):
    student = Student.objects.get(user=request.user)
    payments = Payment.objects.filter(student=student).order_by('-created_at')
    total_paid = payments.filter(status='approved').aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_amount = student.total_fees - total_paid

    context = {
        'student': student,
        'payments': payments,
        'total_paid': total_paid,
        'remaining_amount': remaining_amount,
    }
    return render(request, 'student/payment_history.html', context)

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
