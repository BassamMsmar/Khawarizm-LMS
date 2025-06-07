from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminDashboard.html'

class AnnouncementsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminAnnouncements.html'

class DepartmentsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminDepartments.html'

class CoursesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminCourses.html'

class LecturersView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminLecturers.html'

class StudentsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminStudents.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(user_type='student')
        return context

class ExamsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminExams.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminProfile.html'

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminSettings.html'

class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminAbout.html'
