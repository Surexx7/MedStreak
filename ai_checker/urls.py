from django.urls import path
from . import views

app_name = 'ai_checker'

urlpatterns = [
    path('', views.question_feed, name='question_feed'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('react/question/<int:question_id>/', views.react_to_question, name='react_to_question'),
    path('react/answer/<int:answer_id>/', views.react_to_answer, name='react_to_answer'),
    path('load-more/', views.load_more_questions, name='load_more_questions'),
    
    # Notification URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/count/', views.get_notification_count, name='notification_count'),
    path('notifications/json/', views.notifications_json, name='notifications_json'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]