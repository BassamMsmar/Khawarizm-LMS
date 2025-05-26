from django.views.generic import TemplateView
from .mixins import UserTypeRedirectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class BaseDashboardView(TemplateView):
    """كلاس أساسي يمكن الوراثة منه"""
    template_name = ''  # يتم تحديده في الفروع

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == 'student' and not isinstance(self, StudentDashboardView):
            return redirect('dashboard:student')
        if user.user_type == 'lecturer' and not isinstance(self, LecturerDashboardView):
            return redirect('dashboard:lecturer')
        if user.user_type in ['admin', 'teaching_assistant'] and not isinstance(self, AdminDashboardView):
            return redirect('dashboard:admin')
        return super().dispatch(request, *args, **kwargs)


class StudentDashboardView(UserTypeRedirectMixin, TemplateView):
    template_name = 'dashboard/StudentDashboard/studentDashboard.html'

class LecturerDashboardView(UserTypeRedirectMixin, TemplateView):
    template_name = 'dashboard/LecturerDashboard/lecturerDashboard.html'

class AdminDashboardView(UserTypeRedirectMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminDashboard.html'