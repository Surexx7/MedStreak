"""
URL configuration for MediScope project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cases/', include('cases.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('anatomy/', include('anatomy.urls')),
    path('ai-checker/', include('ai_checker.urls')),
    path('auth/', include('django.contrib.auth.urls')),
     #logout configuration
    path('logout/', 
         auth_views.LogoutView.as_view(
             template_name='registration/logout.html'
         ), 
         name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
