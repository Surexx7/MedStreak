from django.contrib import admin
from .models import Case, CaseStep, Choice, CaseAttempt

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class CaseStepInline(admin.TabularInline):
    model = CaseStep
    extra = 1
    show_change_link = True
    inlines = [ChoiceInline]

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'category', 'total_xp')
    inlines = [CaseStepInline]

@admin.register(CaseStep)
class CaseStepAdmin(admin.ModelAdmin):
    list_display = ('case', 'step_number', 'title')
    inlines = [ChoiceInline]
    list_filter = ('case',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('step', 'text', 'xp_reward', 'is_correct')
    list_filter = ('step__case', 'step')

@admin.register(CaseAttempt)
class CaseAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'case', 'current_step', 'total_xp_earned', 'completed')
    readonly_fields = ('started_at', 'completed_at')