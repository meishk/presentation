from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('setJudges/', views.setJudges, name='setJudges'),
    path('scoring/', views.scoring, name='scoring'),
    path('personnel_info/', views.personnel_info, name='personnel_info'),
    path('follow/', views.follow, name='follow'),
    path('scored/', views.scored, name='scored'),
    path('statistics/', views.statistics, name='statistics'),
    path('update/', views.update, name='update'),
    path('excel/', views.excel, name='excel'),
]