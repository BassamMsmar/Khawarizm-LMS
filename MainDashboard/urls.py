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

    # ____________________________________________________________________________


    path('students/', views.students, name='students'),
    path('students/create/ajax/', views.StudentCreateAjaxView.as_view(), name='create_student_ajax'),
    path('students/update/<int:pk>/', views.StudentUpdateAjaxView.as_view(), name='update_student_ajax'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('students/toggle/<int:pk>/', views.toggle_student_status, name='toggle_student_status'),
   
   
   # ____________________________________________________________________________

    path('teachers/', views.teachers, name='teachers'),
    path('teachers/create/ajax/', views.TeacherCreateAjaxView.as_view(), name='create_teacher_ajax'),
    path('teachers/update/<int:pk>/', views.TeacherUpdateAjaxView.as_view(), name='update_teacher_ajax'),
    path('teachers/delete/<int:pk>/', views.delete_teacher, name='delete_teacher'),


   # ____________________________________________________________________________


    path('quizzes', views.quizzes),
    path('reports', views.reports),
    path('settings', views.settings),
  
]