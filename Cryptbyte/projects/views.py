"""
Cryptbyte Solutions - Projects Application Views

Provides public views for filtering case studies across technical categories and keywords,
as well as detailed case study pages for individual projects.
"""

from django.shortcuts import render, Http404
from django.db.models import Q
from .models import Project


def projects(request):
    """
    Render the public Projects portfolio with category filter tabs and search query.

    Supports:
    - ?category=<slug>: Filters projects by technical domain ('web', 'ai', 'cloud', 'security', 'all').
    - ?q=<keyword>: Case-insensitive search across title, description, stack, and tagline.

    Calculates live counts for each category to populate the filter badges and highlights
    a lead featured project in the hero presentation.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered projects portfolio template.
    """
    category_param = request.GET.get('category', '').strip().lower()
    search_query = request.GET.get('q', '').strip()

    # Query published projects
    projects_qs = Project.objects.filter(is_published=True)

    # Apply search filter
    if search_query:
        projects_qs = projects_qs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(stack__icontains=search_query) |
            Q(tagline__icontains=search_query)
        )

    # Apply category filter
    if category_param and category_param != 'all':
        projects_qs = projects_qs.filter(category=category_param)

    all_projects = list(projects_qs)

    # Determine featured hero project and remaining grid case studies
    featured_project = None
    featured_candidates = [p for p in all_projects if p.is_featured]
    if featured_candidates:
        featured_project = featured_candidates[0]
        grid_projects = [p for p in all_projects if p.id != featured_project.id]
    elif all_projects:
        featured_project = all_projects[0]
        grid_projects = all_projects[1:]
    else:
        grid_projects = []

    # Category badge metrics
    total_db_count = Project.objects.filter(is_published=True).count()
    web_count = Project.objects.filter(is_published=True, category='web').count()
    ai_count = Project.objects.filter(is_published=True, category='ai').count()
    cloud_count = Project.objects.filter(is_published=True, category='cloud').count()
    security_count = Project.objects.filter(is_published=True, category='security').count()

    categories = [
        {'slug': 'all', 'name': 'All Work', 'count': total_db_count},
        {'slug': 'web', 'name': 'Web Apps', 'count': web_count},
        {'slug': 'ai', 'name': 'AI / ML', 'count': ai_count},
        {'slug': 'cloud', 'name': 'Cloud', 'count': cloud_count},
        {'slug': 'security', 'name': 'Security', 'count': security_count},
    ]

    return render(request, 'projects/index.html', {
        'featured_project': featured_project,
        'projects': grid_projects,
        'all_projects': all_projects,
        'categories': categories,
        'current_category': category_param or 'all',
        'search_query': search_query,
        'total_count': len(all_projects),
        'total_db_count': total_db_count,
    })


def project_detail(request, slug):
    """
    Render a comprehensive case study view for an individual project.

    Allows authenticated staff members to preview unpublished draft projects
    while restricting public access exclusively to published work.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        slug (str): Unique URL slug identifier for the Project.

    Returns:
        HttpResponse: Rendered project detail template.

    Raises:
        Http404: If project does not exist or is unpublished for non-staff visitors.
    """
    if request.user.is_staff:
        project = Project.objects.filter(slug=slug).first()
    else:
        project = Project.objects.filter(slug=slug, is_published=True).first()

    if not project:
        raise Http404("Project not found")

    # Fetch other case studies for discovery recommendations
    other_projects = Project.objects.filter(is_published=True).exclude(id=project.id)[:3]

    return render(request, 'projects/detail.html', {
        'project': project,
        'other_projects': other_projects,
    })
