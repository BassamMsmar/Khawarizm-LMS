from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..mixins import UserTypeRedirectMixin

class AdminDashboardView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminDashboard.html'

class AnnouncementsView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminAnnouncements.html'

class DepartmentsView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminDepartments.html'

class CoursesView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminCourses.html'

class LecturersView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminLecturers.html'

class StudentsView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminStudents.html'

class ExamsView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminExams.html'

class ProfileView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminProfile.html'

class SettingsView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminSettings.html'

class AboutView(LoginRequiredMixin, UserTypeRedirectMixin, TemplateView):
    required_user_type = 'admin'
    template_name = 'dashboard/AdminDashboard/adminAbout.html'
