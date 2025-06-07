from django.urls import path, include
from django.http import HttpResponse

from .views.base_views import baseDashboard

app_name = 'dashboard'

def test(request):
    return HttpResponse("Hello")

urlpatterns = [
    # path('', test, name='test'),
    path('', baseDashboard, name='baseDashboard'),
    path('admin/', include('dashboard.urls.admin_urls', namespace='admin')),
    path('staff/', include('dashboard.urls.staff_urls', namespace='staff')),
    path('student/', include('dashboard.urls.student_urls', namespace='student')),
]