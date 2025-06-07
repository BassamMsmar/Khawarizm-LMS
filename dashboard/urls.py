from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    path('admin/', include('dashboard.urls.admin_urls')),
    path('staff/', include('dashboard.urls.staff_urls')),
    path('student/', include('dashboard.urls.student_urls')),
    ]
    