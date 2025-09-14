from django.urls import path
from . import views
from .views import LecturerProfileDetailView, LecturerProfileUpdateView

app_name = 'MainDashboard'

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
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/unit/create/', views.UnitCreateAjaxView.as_view(), name='create_unit_ajax'),
    path('unit/update/<int:pk>/', views.UnitUpdateAjaxView.as_view(), name='update_unit_ajax'),
    path('unit/<int:unit_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('unit/<int:unit_id>/lessons/create/', views.LessonCreateView.as_view(), name='create_lesson'),
    path('lessons/<int:pk>/update/', views.LessonUpdateView.as_view(), name='update_lesson'),
    path('lessons/<int:pk>/delete/', views.delete_lesson, name='delete_lesson'),
    path('unit/<int:unit_id>/quizzes/', views.quiz_list, name='quiz_list'),
    path('unit/<int:unit_id>/quizzes/create/', views.QuizCreateView.as_view(), name='create_quiz'),
    path('quizzes/<int:pk>/update/', views.QuizUpdateView.as_view(), name='update_quiz'),
    path('quizzes/<int:pk>/delete/', views.delete_quiz, name='delete_quiz'),
    path('quizzes/<int:quiz_id>/questions/', views.question_list, name='question_list'),
    path('quizzes/<int:quiz_id>/questions/create/', views.QuestionCreateView.as_view(), name='create_question'),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='update_question'),
    path('questions/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('questions/<int:question_id>/choices/', views.choice_list, name='choice_list'),
    path('questions/<int:question_id>/choices/create/', views.ChoiceCreateView.as_view(), name='create_choice'),
    path('choices/<int:pk>/update/', views.ChoiceUpdateView.as_view(), name='update_choice'),
    # path('choices/<int:pk>/delete/', views.delete_choice, name='delete_choice'),
    path('course/<int:course_id>/lesson/create/', views.LessonCreateAjaxView.as_view(), name='create_lesson_ajax'),
    path('lesson/update/<int:pk>/', views.LessonUpdateAjaxView.as_view(), name='update_lesson_ajax'),
    path('lesson/delete/<int:pk>/', views.delete_lesson, name='delete_lesson'),
    
# ____________________________________________________________________________

    path('dashboard', views.dashboard),
    path('lessons/', views.LessonListView.as_view(), name='lessons'),
    path('lessons/create/ajax/', views.LessonCreateAjaxView.as_view(), name='create_lesson_ajax'),
    path('lessons/update/<int:pk>/', views.LessonUpdateAjaxView.as_view(), name='update_lesson_ajax'),
    path('lessons/delete/<int:pk>/', views.delete_lesson, name='delete_lesson'),
    path('lessons/search/', views.lesson_search_ajax, name='lesson_search_ajax'),

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
    path('profile/', LecturerProfileDetailView.as_view(), name='lecturer-profile'),
    path('profile/update/', LecturerProfileUpdateView.as_view(), name='lecturer-profile-update'),


   # ____________________________________________________________________________

    path('payment-requests/', views.payment_requests, name='payment_requests'),
    path('payment-requests/approve/<int:payment_id>/', views.approve_payment, name='approve_payment'),
    path('payment-requests/reject/<int:payment_id>/', views.reject_payment, name='reject_payment'),

    path('reports', views.reports),
    path('settings', views.settings),
  
]