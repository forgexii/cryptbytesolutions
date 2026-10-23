"""
Cryptbyte Solutions - Teams Application Configuration
"""

from django.apps import AppConfig


class TeamsConfig(AppConfig):
    """Application configuration for the team members and departments module."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teams'

