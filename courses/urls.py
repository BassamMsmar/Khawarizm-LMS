from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('list', views.CourseList.as_view()),
    path('<slug:slug>', views.CourseDetail.as_view(),name='course_detail'),
# ✅ التصحيح
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/', views.Lesson_Detail, name='lesson_detail'),
]


