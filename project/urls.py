from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from about import views
from accounts.views import redirect_user


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('profile/', redirect_user, name='profile'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.base_urls')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('department/', include('department.urls')),
    path('college/', include('college.urls')),
    path('degreeLevel/', include('degreeLevel.urls')),

    path("main-dashboard/", include('MainDashboard.urls')),
    path("student-dashboard/", include('student.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications')), # Added this line


    # path('__debug__/', include(debug_toolbar_urls)),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]