from django.shortcuts import render, Http404
from django.db.models import Q
from .models import Solution


def solutions(request):
    """Public Solutions index page for Cryptbyte Solutions with dynamic DB counts."""
    search_query = request.GET.get('q', '').strip()
    solutions_qs = Solution.objects.filter(is_published=True)

    if search_query:
        solutions_qs = solutions_qs.filter(
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(tagline__icontains=search_query) |
            Q(short_desc__icontains=search_query) |
            Q(technologies__icontains=search_query) |
            Q(overview__icontains=search_query)
        )

    solutions_list = list(solutions_qs)
    total_db_count = Solution.objects.filter(is_published=True).count()

    return render(request, 'solutions/index.html', {
        'solutions': solutions_list,
        'search_query': search_query,
        'total_count': len(solutions_list),
        'total_db_count': total_db_count,
    })


def solution_detail(request, slug):
    """Detailed explanation page for a specific Cryptbyte Solution."""
    solution = Solution.objects.filter(slug=slug, is_published=True).first()
    if not solution:
        raise Http404("Solution not found")

    other_solutions = Solution.objects.filter(is_published=True).exclude(id=solution.id)[:3]

    return render(request, 'solutions/detail.html', {
        'solution': solution,
        'other_solutions': other_solutions,
        'metrics': solution.get_metrics(),
        'challenges': solution.get_challenges(),
        'capabilities': solution.get_capabilities(),
        'roadmap': solution.get_roadmap(),
        'technologies': solution.tech_list,
    })
