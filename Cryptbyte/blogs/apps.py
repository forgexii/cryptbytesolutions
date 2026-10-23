"""
Cryptbyte Solutions - Blogs Application Configuration
"""

from django.apps import AppConfig


class BlogsConfig(AppConfig):
    """Application configuration for the engineering editorial blog module."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogs'

