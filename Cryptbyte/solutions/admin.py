"""
Cryptbyte Solutions - Solutions Django Admin Configuration

Registers the Solution model with category filtering, search, and prepopulated slugs.
"""

from django.contrib import admin
from .models import Solution


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    """Admin interface for managing enterprise product solutions and architectures."""
    list_display = ('title', 'category', 'order', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'tagline', 'short_desc', 'overview', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')
