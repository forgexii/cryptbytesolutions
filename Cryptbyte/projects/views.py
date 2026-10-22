from django.shortcuts import render
from django.db.models import Q
from .models import Project


def projects(request):
    """Public Projects portfolio overview with search and category filtering."""
    category_param = request.GET.get('category', '').strip().lower()
    search_query = request.GET.get('q', '').strip()

    projects_qs = Project.objects.filter(is_published=True)

    if search_query:
        projects_qs = projects_qs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(stack__icontains=search_query) |
            Q(tagline__icontains=search_query)
        )

    if category_param and category_param != 'all':
        projects_qs = projects_qs.filter(category=category_param)

    all_projects = list(projects_qs)

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
