from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.db.models import Q
from department.models import Department
from MainDashboard.forms import DepartmentForm
from accounts.decorators import staff_required
from django.utils.decorators import method_decorator


@method_decorator(staff_required, name='dispatch')
class DepartmentListView(ListView):
    model = Department
    template_name = 'pages/departments.html'
    context_object_name = 'departments'

    def get_queryset(self):
        user = self.request.user
        if user.has_role('admin'):
            return Department.objects.all()
        elif user.has_role('lecturer'):
            if user.department and user.department.college:
                return Department.objects.filter(college=user.department.college)
        return Department.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DepartmentForm() # Add DepartmentForm to context
        return context


@method_decorator(staff_required, name='dispatch')
class DepartmentCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@method_decorator(staff_required, name='dispatch')
class DepartmentUpdateAjaxView(View):
    def get(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(instance=department)
        return JsonResponse({
            'form': form.as_p(),
            'instance': {
                'name': department.name,
                'college': department.college.id if department.college else '',
                'admin': department.admin.id if department.admin else '',
                'is_active': department.is_active,
            }
        })

    def post(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


@staff_required
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('/main-dashboard/departments/')


@staff_required
def department_search_ajax(request):
    search_query = request.GET.get('q', '')
    user = request.user

    if user.has_role('admin'):
        departments = Department.objects.all()
    elif user.has_role('lecturer'):
        if user.department and user.department.college:
            departments = Department.objects.filter(college=user.department.college)
        else:
            departments = Department.objects.none()
    else:
        departments = Department.objects.none()

    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) |
            Q(college__title__icontains=search_query) |
            Q(admin__first_name__icontains=search_query) |
            Q(admin__last_name__icontains=search_query)
        ).distinct()

    department_data = []
    for department in departments:
        department_data.append({
            'id': department.id,
            'slug': department.slug,
            'name': department.name,
            'college': department.college.title if department.college else '',
            'admin': department.admin.get_full_name() if department.admin else '',
            'is_active': department.is_active,
            'created_at': department.created_at.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'departments': department_data})
