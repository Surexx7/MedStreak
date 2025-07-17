from django.contrib import admin
from .models import AnatomySystem, AnatomyStructure, AnatomyProgress


class AnatomyStructureInline(admin.TabularInline):
    model = AnatomyStructure
    extra = 1


class AnatomySystemAdmin(admin.ModelAdmin):
    inlines = [AnatomyStructureInline]
    list_display = ['name', 'color', 'created_at']
    search_fields = ['name', 'description']


class AnatomyStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'system', 'location', 'xp_reward']
    list_filter = ['system']
    search_fields = ['name', 'description', 'function']


class AnatomyProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'structure', 'viewed_at', 'time_spent', 'xp_earned']
    list_filter = ['structure__system', 'viewed_at']
    search_fields = ['user__username', 'structure__name']


admin.site.register(AnatomySystem, AnatomySystemAdmin)
admin.site.register(AnatomyStructure, AnatomyStructureAdmin)
admin.site.register(AnatomyProgress, AnatomyProgressAdmin)
