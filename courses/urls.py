from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('list', views.CourseList.as_view()),
    path('list/<slug:slug>/', views.CourseDetail.as_view(), name='courseDetails'),
]


