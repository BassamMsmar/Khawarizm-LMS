from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'pages/dashboard.html')



from django.views.generic import ListView, View, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from college.models import College
from department.models import Department

from .forms import CourseForm, CollegeForm
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

# ____________________________________________________________________



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
                'regular_price': college.regular_price,
                'discounted_price': college.discounted_price,
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
                'academic_hours': course.academic_hours,
                'short_description': course.short_description,
                'description': course.description,
                'colleges': [college.id for college in course.colleges.all()],
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



from django.shortcuts import get_object_or_404, redirect
from courses.models import Course

def delete_course(request, pk):
    course = Course.objects.get(pk=pk)
    course.delete()
    return redirect('/main-dashboard/courses/')




from django.http import JsonResponse
from django.db.models import Q
from courses.models import Course     

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






def lessons(request):
    return render(request, 'pages/lessons.html')

# ____________________________________________________________________

def quizzes(request):
    return render(request, 'pages/quizzes.html')



# ____________________________________________________________________

def students(request):
    return render(request, 'pages/students.html')


# ____________________________________________________________________



def reports(request):
    return render(request, 'pages/reports.html')



# ____________________________________________________________________


def settings(request):
    return render(request, 'pages/settings.html')