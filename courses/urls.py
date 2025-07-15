from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('list', views.CourseList.as_view()),
    path('<slug:slug>', views.CourseDetail.as_view(),name='course_detail'),

]


