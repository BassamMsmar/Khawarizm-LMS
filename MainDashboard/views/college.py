from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.db.models import Q
from college.models import College
from courses.models import Course
from MainDashboard.forms import CollegeForm
from accounts.decorators import staff_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

User = get_user_model()


@method_decorator(staff_required, name='dispatch')
class CollegeListView(ListView):
    model = College
    template_name = 'pages/colleges.html'
    context_object_name = 'colleges'

    def get_queryset(self):
        user = self.request.user
        if user.has_role('admin'):
            return College.objects.all()
        elif user.has_role('lecturer'):
            if user.department and user.department.college:
                return College.objects.filter(pk=user.department.college.pk)
        return College.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        colleges_with_counts = []
        # Iterate over the queryset returned by get_queryset
        for college in self.get_queryset():
            num_departments = college.departments.count()
            num_courses = Course.objects.filter(department__college=college).count()
            num_teachers = User.objects.filter(department__college=college, profile_type='lecturer').count()
            num_students = User.objects.filter(department__college=college, profile_type='student').count()
            
            colleges_with_counts.append({
                'college': college,
                'num_departments': num_departments,
                'num_courses': num_courses,
                'num_teachers': num_teachers,
                'num_students': num_students,
            })
        
        context['colleges_with_counts'] = colleges_with_counts
        context['form'] = CollegeForm()
        return context


@method_decorator(staff_required, name='dispatch')
class CollegeCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = CollegeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
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


@staff_required
def delete_college(request, pk):
    college = College.objects.get(pk=pk)
    college.delete()
    return redirect('/main-dashboard/college/')


@staff_required
def college_search_ajax(request):
    search_query = request.GET.get('q', '')
    user = request.user

    if user.has_role('admin'):
        colleges = College.objects.all()
    elif user.has_role('lecturer'):
        if user.department and user.department.college:
            colleges = College.objects.filter(pk=user.department.college.pk)
        else:
            colleges = College.objects.none()
    else:
        colleges = College.objects.none()

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
