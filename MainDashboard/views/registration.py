from django.shortcuts import render, redirect, get_object_or_404
from student.models import CourseRegistration
from notifications.models import Notification
from accounts.decorators import staff_required


@staff_required
def course_registration_requests(request):
    pending_registrations = CourseRegistration.objects.filter(status='pending').order_by('-created_at')
    other_registrations = CourseRegistration.objects.exclude(status='pending').order_by('-created_at')
    context = {
        'pending_registrations': pending_registrations,
        'other_registrations': other_registrations,
    }
    return render(request, 'pages/course_registration_requests.html', context)


@staff_required
def approve_registration(request, registration_id):
    registration = get_object_or_404(CourseRegistration, id=registration_id)
    registration.status = 'approved'
    registration.save()
    # Add the student's user to the course's students_enrolled
    course = registration.course
    course.students_enrolled.add(registration.student.user)
    return redirect('course_registration_requests')


@staff_required
def reject_registration(request, registration_id):
    registration = get_object_or_404(CourseRegistration, id=registration_id)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason')
        if reason:
            registration.status = 'rejected'
            registration.save()
            # Send a notification to the student
            Notification.objects.create(
                recipient=registration.student.user,
                message=f'Your request to join the course {registration.course.title} has been rejected. Reason: {reason}'
            )
            return redirect('course_registration_requests')

    context = {
        'registration': registration,
    }
    return render(request, 'pages/reject_registration.html', context)
