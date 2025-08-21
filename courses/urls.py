from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('list/', views.CourseList.as_view(), name='course_list'),
    path('<slug:slug>', views.CourseDetail.as_view(),name='course_detail'),
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/', views.Lesson_Detail, name='lesson_detail'),
    # Quiz URLs
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/', views.quiz_detail, name='quiz_detail'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/take/', views.take_quiz, name='take_quiz'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/result/', views.quiz_result, name='quiz_result'),

    # Quiz CRUD URLs
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    path('quizzes/create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail_crud'),
    path('quizzes/<int:pk>/update/', views.QuizUpdateView.as_view(), name='quiz_update'),
    path('quizzes/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),

    # Question CRUD URLs (nested under Quiz)
    path('quizzes/<int:quiz_pk>/questions/', views.QuestionListView.as_view(), name='question_list'),
    path('quizzes/<int:quiz_pk>/questions/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('quizzes/<int:quiz_pk>/questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('quizzes/<int:quiz_pk>/questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('quizzes/<int:quiz_pk>/questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),

    # Choice CRUD URLs (nested under Question)
    path('questions/<int:question_pk>/choices/', views.ChoiceListView.as_view(), name='choice_list'),
    path('questions/<int:question_pk>/choices/create/', views.ChoiceCreateView.as_view(), name='choice_create'),
    path('questions/<int:question_pk>/choices/<int:pk>/', views.ChoiceDetailView.as_view(), name='choice_detail'),
    path('questions/<int:question_pk>/choices/<int:pk>/update/', views.ChoiceUpdateView.as_view(), name='choice_update'),
    path('questions/<int:question_pk>/choices/<int:pk>/delete/', views.ChoiceDeleteView.as_view(), name='choice_delete'),
]