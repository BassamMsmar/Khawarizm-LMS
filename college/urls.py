
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CollegeList.as_view(), name='collegeList'),
    path('create', views.CollegeCreate.as_view(), name='createCollege'),
    path('<slug:slug>', views.CollegeDetail.as_view(), name='collegeDetail'),
    path('update/<slug:slug>', views.CollegeUpdate.as_view(), name='collegeUpdate'),
    path('delete/<slug:slug>', views.CollegeDelete.as_view(), name='collegeDelete'),
    path('<slug:slug>/departments/', views.CollegeDepartmentList.as_view(), name='college_departments'),
    path('<slug:slug>/courses/', views.CollegeCourseList.as_view(), name='college_courses'),
    path('<slug:slug>/teachers/', views.CollegeTeacherList.as_view(), name='college_teachers'),
    path('<slug:slug>/students/', views.CollegeStudentList.as_view(), name='college_students'),
]
