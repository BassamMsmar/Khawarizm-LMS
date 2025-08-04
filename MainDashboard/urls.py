from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard),
    path('courses', views.courses),
    path('lessons', views.lessons),
    path('students', views.students),
    path('quizzes', views.quizzes),
    path('reports', views.reports),
    path('settings', views.settings),
  
]
