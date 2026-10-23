"""
Cryptbyte Solutions - Teams Django Admin Configuration

Registers Department, Specialization, and TeamMember models for management in the default admin.
"""

from django.contrib import admin
from .models import TeamMember, Department, Specialization


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for managing corporate organizational departments."""
    list_display = ('name', 'slug', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    """Admin interface for managing engineering disciplines and technical specialties."""
    list_display = ('name', 'slug', 'department', 'order')
    list_filter = ('department',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('department', 'order', 'name')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin interface for managing staff records, biographies, leadership status, and credentials."""
    list_display = ('name', 'role', 'department', 'is_leadership', 'order')
    list_filter = ('department', 'is_leadership', 'specializations')
    search_fields = ('name', 'role', 'bio', 'skills')
    ordering = ('order', 'name')
    filter_horizontal = ('specializations',)
