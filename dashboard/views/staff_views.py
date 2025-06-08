from django.views.generic import TemplateView
from dashboard.mixins import RolesRequiredMixin



class StaffDashboardView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/staffDashboard/staffDashboard.html'
    allowed_roles = ['staff']