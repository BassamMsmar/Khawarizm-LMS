from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
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
    student = Student.objects.get(user=request.user)
    department = student.department
    payments = Payment.objects.filter(student=student)
    total_paid = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    remaining_amount = student.total_fees - total_paid

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = student
            payment.save()
            return redirect('student:my_payments')
    else:
        form = PaymentForm()

    context = {
        'student': student,
        'department': department,
        'payments': payments,
        'total_paid': total_paid,
        'remaining_amount': remaining_amount,
        'form': form
    }
    return render(request, 'student/my_payments.html', context)

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
