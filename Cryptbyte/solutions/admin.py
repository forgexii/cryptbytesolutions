from django.contrib import admin
from .models import Solution


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'tagline', 'short_desc', 'overview', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')
