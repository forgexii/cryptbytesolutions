"""
Cryptbyte Solutions - Solutions Application Views

Provides public catalog views for exploring enterprise software solutions,
as well as detailed architecture breakdown pages for individual offerings.
"""

from django.shortcuts import render, Http404
from django.db.models import Q
from .models import Solution


def solutions(request):
    """
    Render the public solutions catalog with keyword search.

    Supports:
    - ?q=<keyword>: Case-insensitive query across title, category, tagline, short description,
      technologies, and technical overview text.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered solutions catalog page.
    """
    search_query = request.GET.get('q', '').strip()
    solutions_qs = Solution.objects.filter(is_published=True)

    # Apply search filter if query string provided
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
    """
    Render an architectural deep-dive page for a specific Solution.

    Allows authenticated staff members to preview unpublished draft solutions
    while ensuring the general public accesses only active offerings.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        slug (str): Unique URL slug identifier for the Solution.

    Returns:
        HttpResponse: Rendered solution detail case study template.

    Raises:
        Http404: If solution does not exist or is unpublished for non-staff visitors.
    """
    if request.user.is_staff:
        solution = Solution.objects.filter(slug=slug).first()
    else:
        solution = Solution.objects.filter(slug=slug, is_published=True).first()

    if not solution:
        raise Http404("Solution not found")

    # Fetch other active solutions for exploratory recommendation carousel
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
