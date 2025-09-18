from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('redirect/', views.redirect_user, name='user_redirect'),
]
