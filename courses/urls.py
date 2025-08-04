from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('list/', views.CourseList.as_view(), name='course_list'),
    path('<slug:slug>', views.CourseDetail.as_view(),name='course_detail'),
# ✅ التصحيح
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/', views.Lesson_Detail, name='lesson_detail'),
    # Quiz URLs
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/', views.quiz_detail, name='quiz_detail'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/take/', views.take_quiz, name='take_quiz'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/result/', views.quiz_result, name='quiz_result'),
]


