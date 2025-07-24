from django.urls import path
from ..views.admin_views import AdminDashboardView, AnnouncementsView, CreateCourseView,CollegesView, DepartmentsView, CoursesView, LecturersView, StudentsView, ExamsView, ProfileView, SettingsView, AboutView

app_name = 'admin'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='adminDashboard'),
    path('announcements/', AnnouncementsView.as_view(), name='adminAnnouncements'),
    path('colleges/', CollegesView.as_view(), name='adminColleges'),
    path('departments/', DepartmentsView.as_view(), name='adminDepartments'),
    path('courses/', CoursesView.as_view(), name='adminCourses'),
    path('courses/create/', CreateCourseView.as_view(), name='create_course'),

    path('lecturers/', LecturersView.as_view(), name='adminLecturers'),
    path('students/', StudentsView.as_view(), name='adminStudents'),
    path('exams/', ExamsView.as_view(), name='adminExams'),
    path('profile/', ProfileView.as_view(), name='adminProfile'),
    path('settings/', SettingsView.as_view(), name='adminSettings'),
    path('about/', AboutView.as_view(), name='adminAbout'),
    ]