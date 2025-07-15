from site import venv
from django.urls import path
from . import views

urlpatterns = [
    path('', views.collegeList, name='collegeList'),
    path('createCollege', views.createCollege, name='createCollege'),
    path('collegeDetail', views.collegeDetail, name='collegeDetail'),
    path('collegeUpdate', views.collegeUpdate, name='collegeUpdate'),
    path('collegeDelete', views.collegeDelete, name='collegeDelete'),
    
]
