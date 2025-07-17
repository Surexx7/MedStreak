from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, QuizAnswer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'quiz', 'points', 'order']
    list_filter = ['quiz']


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'difficulty', 'time_limit', 'xp_reward', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['title', 'description']


class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'max_score', 'percentage', 'completed_at']
    list_filter = ['quiz', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['percentage']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuizAnswer)
