from django.contrib import admin
from .models import Question, Answer, QuestionReaction, AnswerReaction

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'get_answers_count', 'get_reactions_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_answers_count(self, obj):
        return obj.get_answers_count()
    get_answers_count.short_description = 'Answers'
    
    def get_reactions_count(self, obj):
        return obj.get_reactions_count()
    get_reactions_count.short_description = 'Reactions'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'created_at', 'content_preview']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'question__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(QuestionReaction)
class QuestionReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    search_fields = ['user__username', 'question__title']

@admin.register(AnswerReaction)
class AnswerReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    search_fields = ['user__username', 'answer__content']