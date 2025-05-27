from django.views.generic import TemplateView
from ..mixins import UserTypeRedirectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect



class LecturerDashboardView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    template_name = 'dashboard/LecturerDashboard/lecturerDashboard.html'