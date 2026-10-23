"""
Cryptbyte Solutions - Home Application Views

Renders the primary landing page with live database statistics reflecting firm scale.
"""

from django.shortcuts import render
from projects.models import Project
from solutions.models import Solution
from teams.models import TeamMember
from blogs.models import BlogPost


def home(request):
    """
    Render the public homepage with real-time portfolio and organizational metrics.

    Calculates live counts for published projects, solutions, team specialists,
    and engineering articles to supply the animated hero counters.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered homepage with live metrics context.
    """
    # Fetch live counts of active public resources
    projects_count = Project.objects.filter(is_published=True).count()
    solutions_count = Solution.objects.filter(is_published=True).count()
    team_count = TeamMember.objects.count()
    blogs_count = BlogPost.objects.filter(is_published=True).count()

    return render(request, 'home/index.html', {
        'projects_count': projects_count,
        'solutions_count': solutions_count,
        'team_count': team_count,
        'blogs_count': blogs_count,
    })
