from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    path('admin/', include('dashboard.urls.admin_urls')),
    path('lecturer/', include('dashboard.urls.lecturer_urls')),
    path('department_manager/', include('dashboard.urls.department_manager_urls')),
    path('college_manager/', include('dashboard.urls.college_manager_urls')),
    path('student/', include('dashboard.urls.student_urls')),
    ]
    