from django.shortcuts import render
from projects.models import Project
from solutions.models import Solution
from teams.models import TeamMember, Department, Specialization
from blogs.models import BlogPost


def about(request):
    """Public About page for Cryptbyte Solutions with live DB figures."""
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
