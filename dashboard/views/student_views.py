from django.views.generic import TemplateView
from dashboard.mixins import RolesRequiredMixin




class StudentDashboardView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/StudentDashboard/studentDashboard.html'
    allowed_roles = ['student']
