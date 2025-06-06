from django.urls import path
from ..views.college_manager_views import CollegeManagerDashboardView, AnnouncementsView, DepartmentsView, CoursesView, LecturersView, StudentsView, ExamsView, ProfileView, SettingsView, AboutView

app_name = 'dashboard_college_manager'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='adminDashboard'),

    ]