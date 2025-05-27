from django.urls import path
from ..views.lecturer_views import LecturerDashboardView

app_name = 'lecturer'

urlpatterns = [
    path('', LecturerDashboardView.as_view(), name='lecturerDashboard'),
    ]