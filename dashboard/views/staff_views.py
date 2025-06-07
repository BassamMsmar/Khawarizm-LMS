from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/staffDashboard/staffDashboard.html'