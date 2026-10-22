from django.shortcuts import render
from projects.models import Project
from solutions.models import Solution
from teams.models import TeamMember
from blogs.models import BlogPost


def home(request):
    """Public-facing home page for Cryptbyte Solutions with dynamic DB figures."""
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
