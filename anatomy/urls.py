from django.urls import path
from . import views

urlpatterns = [
    path('', views.anatomy_explorer, name='anatomy_explorer'),
    path('home/', views.anatomy_home, name='anatomy_home'),
    path('system/<int:system_id>/', views.system_detail, name='anatomy_system_detail'),
    path('structure/<int:structure_id>/', views.structure_detail, name='anatomy_structure_detail'),
    path('update-time/', views.update_time_spent, name='anatomy_update_time'),
]
