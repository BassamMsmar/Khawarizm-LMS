from django.views.generic import TemplateView
from dashboard.mixins import RolesRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User
from college.models import College
from department.models import Department
from django.db.models import Count
from profiles.models import StudentProfile, LecturerProfile
from courses.models import Course

class AdminDashboardView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminDashboard.html'
    allowed_roles = ['admin']

class AnnouncementsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminAnnouncements.html'
    allowed_roles = ['admin']

class CollegesView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminColleges.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # إجمالي عدد الطلاب في النظام
        total_students = StudentProfile.objects.count()

        # جلب الكليات مع التعدادات المطلوبة
        colleges = College.objects.annotate(
            department_count=Count('departments', distinct=True),
            course_count=Count('courses', distinct=True),
            lecturer_count=Count('lecturer_profiles', distinct=True),
            student_count=Count('student_profiles', distinct=True),
        )

        # حساب نسبة الطلاب لكل كلية
        for college in colleges:
            college.student_ratio = (
                round((college.student_count / total_students * 100), 2)
                if total_students > 0 else 0
            )

        context['colleges'] = colleges
        context['total_students'] = total_students
        return context
class DepartmentsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminDepartments.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.annotate(
            course_count=Count('courses', distinct=True),
            lecturer_count=Count('lecturer_profiles', distinct=True),
            student_count=Count('student_profiles', distinct=True),
        )
        return context

class CoursesView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminCourses.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class LecturersView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminLecturers.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = LecturerProfile.objects.all()
        return context

class StudentsView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminStudents.html'
    allowed_roles = ['admin']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = StudentProfile.objects.all()
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
