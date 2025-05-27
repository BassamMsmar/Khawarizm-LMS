from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    path('admin/', include('dashboard.urls.admin_urls')),
    path('lecturer/', include('dashboard.urls.lecturer_urls')),
    path('student/', include('dashboard.urls.student_urls')),
    ]
    