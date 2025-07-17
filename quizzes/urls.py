from django.urls import path
from . import views
app_name = 'quizzes' 
urlpatterns = [
    
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    path('submit-timed-results/', views.submit_timed_results, name='submit_timed_results'),
    path('timed-challenge/', views.timed_challenge, name='timed_challenge'),

]
