from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class BaseDashboardView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('accounts:login')
            
        if user.profile_type == 'student':
            return redirect('dashboard:student:studentDashboard')
        elif user.profile_type == 'staff':
            return redirect('dashboard:staff:staffDashboard')
        elif user.profile_type == 'admin':
            return redirect('dashboard:admin:adminDashboard')
            
        return super().dispatch(request, *args, **kwargs)


