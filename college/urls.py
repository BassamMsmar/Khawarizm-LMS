
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CollegeList.as_view(), name='collegeList'),
    path('create', views.CollegeCreate.as_view(), name='createCollege'),
    path('<slug:slug>', views.CollegeDetail.as_view(), name='collegeDetail'),
    path('update/<slug:slug>', views.CollegeUpdate.as_view(), name='collegeUpdate'),
    path('delete/<slug:slug>', views.CollegeDelete.as_view(), name='collegeDelete'),
    
]
