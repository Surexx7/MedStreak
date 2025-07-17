from django.contrib import admin
from .models import StudentProfile, Achievement, Activity, StudySession

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'university', 'year_of_study', 'level', 'total_xp', 'current_streak']
    list_filter = ['year_of_study', 'specialization', 'level', 'university']
    search_fields = ['user__username', 'user__email', 'student_id', 'university']
    readonly_fields = ['total_xp', 'level', 'current_streak', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'student_id', 'university', 'year_of_study', 'specialization')
        }),
        ('Gamification', {
            'fields': ('total_xp', 'level', 'current_streak', 'longest_streak')
        }),
        ('Academic Progress', {
            'fields': ('cases_completed', 'quiz_accuracy', 'total_study_time')
        }),
        ('Settings', {
            'fields': ('is_profile_complete', 'email_notifications', 'public_profile')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'achievement_type', 'xp_reward', 'earned_at']
    list_filter = ['achievement_type', 'earned_at']
    search_fields = ['user__username', 'title']
    date_hierarchy = 'earned_at'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'activity_type', 'xp_earned', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'title']
    date_hierarchy = 'created_at'

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'duration_minutes', 'xp_earned', 'activities_completed']
    list_filter = ['start_time']
    search_fields = ['user__username']
    date_hierarchy = 'start_time'
