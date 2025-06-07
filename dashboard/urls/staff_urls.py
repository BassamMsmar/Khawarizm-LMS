from django.urls import path
from ..views.staff_views import StaffDashboardView

app_name = 'staff'

urlpatterns = [
    path('', StaffDashboardView.as_view(), name='staffDashboard'),
    ]