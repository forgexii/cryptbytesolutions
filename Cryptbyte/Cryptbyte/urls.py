"""
Cryptbyte Solutions - Main URL Configuration

Directs incoming HTTP requests to dedicated application routing modules:
- admin/: Django administrative dashboard.
- home/: Landing page and core firm overview.
- about/: Corporate mission, engineering pillars, and statistics.
- services/: Technical service offerings and architectural capabilities.
- solutions/: Modular product solutions and domain case breakdowns.
- projects/: Portfolio case studies and live client demonstrations.
- teams/: Staff directory, leadership profiles, and specialization filters.
- blogs/: Engineering insights, tech articles, and category archives.
- contact/: Communication channels and enquiry dispatch.
- dashboard/: Internal staff management portal with secure authentication and CRUD.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Built-in Django administrative panel
    path('admin/', admin.site.urls),

    # Public-facing commercial and informational routes
    path('', include('home.urls')),
    path('about/', include('about.urls')),
    path('services/', include('services.urls')),
    path('solutions/', include('solutions.urls')),
    path('projects/', include('projects.urls')),
    path('teams/', include('teams.urls')),
    path('blogs/', include('blogs.urls')),
    path('contact/', include('contact.urls')),

    # Internal staff administration and content management portal
    path('dashboard/', include('dashboard.urls')),
]

# Development media serving (in production, media is served by reverse proxy or cloud storage)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
