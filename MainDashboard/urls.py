from django.urls import path
from . import views

urlpatterns = [
    
    path('college/', views.CollegeListView.as_view(), name='colleges'),
    path('college/create/ajax/', views.CollegeCreateAjaxView.as_view(), name='create_college_ajax'),
    path('college/update/<int:pk>/', views.CollegeUpdateAjaxView.as_view(), name='update_college_ajax'),
    path('college/delete/<int:pk>/', views.delete_college, name='delete_college'),
    path('college/search/', views.college_search_ajax, name='college_search_ajax'),

# ____________________________________________________________________________

    path('departments/', views.DepartmentListView.as_view(), name='departments'),
    path('departments/create/ajax/', views.DepartmentCreateAjaxView.as_view(), name='create_department_ajax'),
    path('departments/update/<int:pk>/', views.DepartmentUpdateAjaxView.as_view(), name='update_department_ajax'),
    path('departments/delete/<int:pk>/', views.delete_department, name='delete_department'),
    path('departments/search/', views.department_search_ajax, name='department_search_ajax'),


# ____________________________________________________________________________

    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/create/ajax/', views.CourseCreateAjaxView.as_view(), name='create_course_ajax'),
    path('courses/update/<int:pk>/', views.CourseUpdateAjaxView.as_view(), name='update_course_ajax'),
    path('courses/delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('courses/search/', views.course_search_ajax, name='course_search_ajax'),
# ____________________________________________________________________________

    path('dashboard', views.dashboard),
    path('lessons', views.lessons),
    path('students', views.students),
    path('quizzes', views.quizzes),
    path('reports', views.reports),
    path('settings', views.settings),
  
]
