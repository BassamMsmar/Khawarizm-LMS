from django.urls import path
from . import views

urlpatterns = [
    path('', views.departmentList, name='departmentList'),
    path('createDepartment', views.createDepartment, name='createDepartment'),
    path('departmentDetail', views.departmentDetail, name='departmentDetail'),
    path('departmentUpdate', views.departmentUpdate, name='departmentUpdate'),
    path('departmentDelete', views.departmentDelete, name='departmentDelete'),
    
]
