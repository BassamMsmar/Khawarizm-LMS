from django.views.generic import TemplateView
from dashboard.mixins import RolesRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User
from college.models import College
from department.models import Department
from django.db.models import Count, Prefetch
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


# views.py

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from courses.models import Course
from ..forms import CourseForm

class CreateCourseView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'dashboard/AdminDashboard/create_course.html'
    success_url = "/dashboard/admin/courses"

    def form_valid(self, form):
        print("Course saved:", form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)





class LecturersView(RolesRequiredMixin, TemplateView):
    template_name = 'dashboard/AdminDashboard/adminLecturers.html'
    allowed_roles = ['admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # تحسين الاستعلام لاحتساب عدد الطلاب لكل مقرر
        courses_prefetch = Prefetch(
            'courses',
            queryset=Course.objects.annotate(
                enrolled_count=Count('students_enrolled')
            ),
            to_attr='lecturer_courses'
        )

        books_prefetch = Prefetch()
        
        # جلب البيانات مع التحسينات
        lecturers = LecturerProfile.objects.prefetch_related(
            courses_prefetch,
            Prefetch('departments', queryset=Department.objects.only('name')),
            Prefetch('colleges', queryset=College.objects.only('name'))
        ).select_related('user').annotate(
            total_students=Count('courses__students_enrolled', distinct=True)
        )
        
        # حساب الإجمالي العام لجميع الطلاب (اختياري)
        total_all_students = Course.objects.aggregate(
            total=Count('students_enrolled', distinct=True)
        )['total']
        
        context.update({
            'profiles': lecturers,
            'total_all_students': total_all_students
        })
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
