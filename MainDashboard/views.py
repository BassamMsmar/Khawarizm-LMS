from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'pages/dashboard.html')



from django.views.generic import ListView, View, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from .forms import CourseForm
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

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



class CourseDeleteAjaxView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


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




def lessons(request):
    return render(request, 'pages/lessons.html')


def quizzes(request):
    return render(request, 'pages/quizzes.html')

def students(request):
    return render(request, 'pages/students.html')


def reports(request):
    return render(request, 'pages/reports.html')


def settings(request):
    return render(request, 'pages/settings.html')