from django.urls import path
from . import views

urlpatterns = [
    path('listDegreeLevel', views.degreeLevelList, name='degreeLevelList'),
    path('createDegreeLevel', views.createDegreeLevel, name='createDegreeLevel'),
    path('updateDegreeLevel', views.updateDegreeLevel, name='updateDegreeLevel'),
    path('deleteDegreeLevel', views.deleteDegreeLevel, name='deleteDegreeLevel'),
]