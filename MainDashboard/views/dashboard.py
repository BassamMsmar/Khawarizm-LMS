from django.shortcuts import render
from courses.models import Course, Lesson
from accounts.models import User
from accounts.decorators import staff_required, lecturer_required


@staff_required
# @lecturer_required
def dashboard(request):
    if request.user.is_staff:
        courses_count = Course.objects.count()
        students_count = User.objects.filter(roles__name__iexact='student').count()
        lessons_count = Lesson.objects.count()
    else:
        courses_count = Course.objects.filter(lecturer=request.user).count()
        students_count = User.objects.filter(enrolled_courses__lecturer=request.user).distinct().count()
        lessons_count = Lesson.objects.filter(course__lecturer=request.user).count()

    context = {
        'courses_count': courses_count,
        'students_count': students_count,
        'lessons_count': lessons_count,
    }

    return render(request, 'pages/dashboard.html', context)
