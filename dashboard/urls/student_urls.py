from django.urls import path, include
from ..views.student_views import StudentDashboardView

app_name = 'student'

urlpatterns = [
    path('', StudentDashboardView.as_view(), name='studentDashboard'),
    ]