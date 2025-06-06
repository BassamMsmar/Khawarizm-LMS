from django.views.generic import TemplateView
from ..mixins import UserTypeRedirectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class BaseDashboardView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    """كلاس أساسي يمكن الوراثة منه"""
    template_name = ''  # يتم تحديده في الفروع

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.roles == 'student' and not isinstance(self, StudentDashboardView):
            return redirect('dashboard:student')
        if user.roles == 'lecturer' and not isinstance(self, LecturerDashboardView):
            return redirect('dashboard:lecturer')
        if user.roles == 'department_manager' and not isinstance(self, DepartmentManagerDashboardView):
            return redirect('dashboard:department_manager')
        if user.roles == 'college_manager' and not isinstance(self, CollegeManagerDashboardView):
            return redirect('dashboard:college_manager')
        if user.roles == 'admin' and not isinstance(self, AdminDashboardView):
            return redirect('dashboard:adminDashboard')
        return super().dispatch(request, *args, **kwargs)


