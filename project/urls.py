"""
URL configuration for project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from about import views
from debug_toolbar import urls as debug_toolbar_urls


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.base_urls')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('department/', include('department.urls')),
    path('college/', include('college.urls')),
    path('degreeLevel/', include('degreeLevel.urls')),

    path("main-dashboard/", include('MainDashboard.urls')),
    path("student-dashboard/", include('student.urls')),


    path('', include('HiStudyApp.urls')),
    path('__debug__/', include(debug_toolbar_urls)),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
