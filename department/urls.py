from django.urls import path
from . import views

urlpatterns = [
    path('', views.DepartmentList.as_view(), name='departmentList'),
    path('create/', views.DepartmentCreate.as_view(), name='createDepartment'),
    path('<slug:slug>/', views.DepartmentDetail.as_view(), name='departmentDetail'),
    path('update/<slug:slug>/', views.DepartmentUpdate.as_view(), name='departmentUpdate'),
    path('delete/<slug:slug>/', views.DepartmentDelete.as_view(), name='departmentDelete'),
]
