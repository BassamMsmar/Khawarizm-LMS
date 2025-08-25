from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('academic-program/', views.academic_program, name='academic_program'),
    path('my-payments/', views.my_payments, name='my_payments'),
    path('notifications/', views.notifications, name='notifications'),
    path('my-grades/', views.my_grades, name='my_grades'),
    path('calendar/', views.calendar, name='calendar'),
    path('settings/', views.settings, name='settings'),
]