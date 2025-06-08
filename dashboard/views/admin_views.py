from django.views.generic import TemplateView
from dashboard.mixins import RolesRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User

class AdminDashboardView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminDashboard.html'
    allowed_roles = ['admin']

class AnnouncementsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminAnnouncements.html'
    allowed_roles = ['admin']

class DepartmentsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminDepartments.html'
    allowed_roles = ['admin']

class CoursesView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminCourses.html'
    allowed_roles = ['admin']

class LecturersView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminLecturers.html'
    allowed_roles = ['admin']

class StudentsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminStudents.html'
    allowed_roles = ['admin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(user_type='student')
        return context

class ExamsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminExams.html'
    allowed_roles = ['admin']

class ProfileView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminProfile.html'
    allowed_roles = ['admin']

class SettingsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminSettings.html'
    allowed_roles = ['admin']

class AboutView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminAbout.html'
    allowed_roles = ['admin']
