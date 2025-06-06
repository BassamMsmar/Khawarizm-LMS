from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..mixins import UserTypeRedirectMixin

from accounts.models import User

class CollegeManagerDashboardView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'college_manager'
    template_name = 'dashboard/CollegeManagerDashboard/collegeManagerDashboard.html'
