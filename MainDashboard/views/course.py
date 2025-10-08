from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.db.models import Q
from courses.models import Course, Unit
from MainDashboard.forms import CourseForm, UnitForm, LessonForm, QuizForm
from accounts.decorators import staff_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

User = get_user_model()


@staff_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    unit_form = UnitForm()
    lesson_form = LessonForm()
    quiz_form = QuizForm()
    context = {
        'course': course,
        'unit_form': unit_form,
        'lesson_form': lesson_form,
        'quiz_form': quiz_form
    }
    return render(request, 'pages/course_detail.html', context)


@method_decorator(staff_required, name='dispatch')
class UnitCreateAjaxView(View):
    def post(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.course = course
            last_unit = course.maindashboard_units.all().order_by('-order').first()
            if last_unit:
                unit.order = last_unit.order + 1
            else:
                unit.order = 1
            unit.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
class UnitUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        unit = get_object_or_404(Unit, pk=pk)
        form = UnitForm(instance=unit)
        return JsonResponse({
            'form': form.as_p()
        })

    def post(self, request, pk, *args, **kwargs):
        unit = get_object_or_404(Unit, pk=pk)
        form = UnitForm(request.POST, request.FILES, instance=unit)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@staff_required
def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    course_id = unit.course.id
    unit.delete()
    return redirect('course_detail', course_id=course_id)


@method_decorator(staff_required, name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'pages/courses.html'
    context_object_name = 'courses'
    def get_queryset(self):
            user = self.request.user
            if user.is_staff:
                return Course.objects.all()
            elif hasattr(user, 'roles') and user.roles.filter(name='lecturer').exists():
                return Course.objects.filter(lecturer=user)
            return Course.objects.none()

@method_decorator(staff_required, name='dispatch')
class CourseCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
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


@staff_required
def delete_course(request, pk):
    course = Course.objects.get(pk=pk)
    course.delete()
    return redirect('/main-dashboard/courses/')


@staff_required
def course_search_ajax(request):
    search_query = request.GET.get('q', '')
    user = request.user
    if user.is_staff:
        courses = Course.objects.all()
    elif hasattr(user, 'roles') and user.roles.filter(name='lecturer').exists():
        courses = Course.objects.filter(lecturer=user)
    else:
        courses = Course.objects.none()

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
