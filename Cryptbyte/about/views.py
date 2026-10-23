"""
Cryptbyte Solutions - About Application Views

Presents firm mission, engineering pillars, technical credentials, and department metrics.
"""

from django.shortcuts import render
from projects.models import Project
from solutions.models import Solution
from teams.models import TeamMember, Department, Specialization
from blogs.models import BlogPost


def about(request):
    """
    Render the public About page with organizational credentials and figures.

    Supplies metrics for firm scale, active engineering departments,
    technical specializations, and thought leadership articles.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered About page with firm statistics context.
    """
    # Compute aggregate metrics across all active domains
    projects_count = Project.objects.filter(is_published=True).count()
    solutions_count = Solution.objects.filter(is_published=True).count()
    team_count = TeamMember.objects.count()
    dept_count = Department.objects.count()
    specs_count = Specialization.objects.count()
    articles_count = BlogPost.objects.filter(is_published=True).count()

    return render(request, 'about/index.html', {
        'projects_count': projects_count,
        'solutions_count': solutions_count,
        'team_count': team_count,
        'dept_count': dept_count,
        'specs_count': specs_count,
        'articles_count': articles_count,
    })
