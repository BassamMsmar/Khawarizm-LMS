from django.shortcuts import redirect
from django.views import View
class UserTypeRedirectMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('login') 

        if user.is_authenticated:
            from .views import StudentDashboardView, LecturerDashboardView, AdminDashboardView
            if user.user_type == 'student' and not isinstance(self, StudentDashboardView):
                return redirect('dashboard:student')
            elif user.user_type == 'lecturer' and not isinstance(self, LecturerDashboardView):
                return redirect('dashboard:lecturer')
            elif user.user_type == 'admin' and not isinstance(self, AdminDashboardView):
                return redirect('dashboard:adminDashboard')

        return super().dispatch(request, *args, **kwargs)
