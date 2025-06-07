from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin




class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/StudentDashboard/studentDashboard.html'
