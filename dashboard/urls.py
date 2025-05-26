from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.AdminDashboardView.as_view(), name='adminDashboard'),
    path('lecturer/', views.LecturerDashboardView.as_view(), name='lecturerDashboard'),
    path('student/', views.StudentDashboardView.as_view(), name='studentDashboard'),
    ]
    