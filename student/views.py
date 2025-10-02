from django.shortcuts import render, redirect

from accounts.decorators import student_required
from courses.models import Course, Unit
from .models import Student, Payment
from .forms import PaymentForm
from django.db.models import Sum

@student_required
def index(request):
    enrolled_courses = request.user.enrolled_courses.all()
    context = {
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'student/index.html', context)

@student_required
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

@student_required
def academic_program(request):
    student = Student.objects.get(user=request.user)
    student_department = request.user.department
    department_courses = []
    enrolled_courses_ids = request.user.enrolled_courses.values_list('id', flat=True)
    
    # Get course registration requests
    registration_requests = CourseRegistration.objects.filter(student=student)
    registration_status = {req.course.id: req.status for req in registration_requests}

    if student_department:
        department_courses = Course.objects.filter(department=student_department)
        
    context = {
        'student_department': student_department,
        'department_courses': department_courses,
        'enrolled_courses_ids': list(enrolled_courses_ids),
        'registration_status': registration_status,
    }
    return render(request, 'student/academic_program.html', context)

@student_required
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

@student_required
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

@student_required
def notifications(request):
    notifications = request.user.notifications.all()
    context = {
        'notifications': notifications,
    }
    return render(request, 'student/notifications.html', context)

@student_required
def my_grades(request):
    return render(request, 'student/my_grades.html')

@student_required
def calendar(request):
    return render(request, 'student/calendar.html')

@student_required
def settings(request):
    return render(request, 'student/settings.html')

from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from profiles.models import StudentProfile
from student.models import Student
from dashboard.mixins import RolesRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()

class StudentDetail(DetailView):
    model = User
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_user = self.get_object()
        context['enrolled_courses'] = student_user.enrolled_courses.all()
        return context

@student_required
def id_card(request):
    student = Student.objects.get(user=request.user)
    student_profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    context = {
        'student': student,
        'student_profile': student_profile,
    }
    return render(request, 'student/id_card.html', context)


@method_decorator(student_required, name='dispatch')
class StudentProfileDetailView(DetailView):
    model = User
    template_name = 'student/student_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_profile'], _ = StudentProfile.objects.get_or_create(user=self.request.user)
        context['student'], _ = Student.objects.get_or_create(user=self.request.user)
        return context

@method_decorator(student_required, name='dispatch')
class StudentProfileUpdateView(UpdateView):
    model = StudentProfile
    fields = ['bio', 'profile_picture', 'country', 'city', 'address', 'postal_code', 'certificate_number', 'certificate_file', 'languages']
    template_name = 'student/student_profile_update.html'
    success_url = reverse_lazy('student:student-profile')

    def get_object(self, queryset=None):
        return StudentProfile.objects.get_or_create(user=self.request.user)[0]

from .models import CourseRegistration

@student_required
def enroll_courses(request):
    if request.method == 'POST':
        course_ids = request.POST.getlist('courses')
        student = Student.objects.get(user=request.user)
        for course_id in course_ids:
            try:
                course = Course.objects.get(id=course_id)
                # Create a course registration request
                CourseRegistration.objects.create(student=student, course=course)
            except Course.DoesNotExist:
                pass
        return redirect('student:my_courses')
    return redirect('student:academic_program')
