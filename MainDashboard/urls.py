from django.urls import path
from . import views

urlpatterns = [
    
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/create/ajax/', views.CourseCreateAjaxView.as_view(), name='create_course_ajax'),
    path('courses/update/<int:pk>/', views.CourseUpdateAjaxView.as_view(), name='update_course_ajax'),
    path('courses/delete/<int:pk>/', views.CourseDeleteAjaxView.as_view(), name='delete_course_ajax'),
    path('courses/search/', views.course_search_ajax, name='course_search_ajax'),

    path('dashboard', views.dashboard),
    path('lessons', views.lessons),
    path('students', views.students),
    path('quizzes', views.quizzes),
    path('reports', views.reports),
    path('settings', views.settings),
  
]
