"""
Cryptbyte Solutions - Projects Django Admin Configuration

Registers the Project model with category filtering, search, and prepopulated slug mapping.
"""

from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for managing engineering portfolio case studies."""
    list_display = ('title', 'category', 'is_featured', 'is_published', 'order', 'created_at')
    list_filter = ('category', 'is_featured', 'is_published')
    search_fields = ('title', 'tagline', 'description', 'stack')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', '-created_at')
