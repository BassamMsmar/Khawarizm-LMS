from django.urls import path
from . import views
from .views import StudentProfileDetailView, StudentProfileUpdateView

app_name = 'student'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('academic-program/', views.academic_program, name='academic_program'),
    path('my-payments/', views.my_payments, name='my_payments'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('notifications/', views.notifications, name='notifications'),
    path('my-grades/', views.my_grades, name='my_grades'),
    path('calendar/', views.calendar, name='calendar'),
    path('settings/', views.settings, name='settings'),
    path('id-card/', views.id_card, name='id_card'),
    path('profile/', StudentProfileDetailView.as_view(), name='student-profile'),
    path('profile/update/', StudentProfileUpdateView.as_view(), name='student-profile-update'),
]