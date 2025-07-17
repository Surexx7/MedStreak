from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_list, name='case_list'),
    path('<int:case_id>/start/', views.start_case, name='start_case'),
    path('attempt/<int:attempt_id>/', views.case_step, name='case_step'),
    path('attempt/<int:attempt_id>/submit/', views.submit_choice, name='submit_choice'),
    path('attempt/<int:attempt_id>/complete/', views.case_complete, name='case_complete'),
]
