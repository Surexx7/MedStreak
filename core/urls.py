from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('start-study-session/', views.start_study_session, name='start_study_session'),
    path('end-study-session/', views.end_study_session, name='end_study_session'),
]
