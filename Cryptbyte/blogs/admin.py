from django.contrib import admin
from .models import BlogPost, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_date', 'is_featured', 'is_published')
    list_filter = ('category', 'is_featured', 'is_published', 'published_date')
    search_fields = ('title', 'excerpt', 'content', 'author', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_date', '-created_at')
