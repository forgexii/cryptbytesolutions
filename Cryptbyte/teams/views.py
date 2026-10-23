"""
Cryptbyte Solutions - Teams Application Views

Provides public views for exploring engineering leadership, department rosters,
specialization filters, and individual member profiles with portfolios.
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import TeamMember, Department, Specialization


def team_list(request):
    """
    Render the public Team directory with department, specialization, and search filters.

    Supports dynamic filtering:
    - ?q=<keyword>: Case-insensitive search across name, role, bio, skills, and department.
    - ?department=<slug>: Filters members belonging to a specific department.
    - ?specialization=<slug>: Filters members possessing a specific technical specialization.

    Divides members into leadership and specialists for clear hierarchical presentation.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered teams directory template.
    """
    search_query = request.GET.get('q', '').strip()
    dept_slug = request.GET.get('department', '').strip().lower()
    spec_slug = request.GET.get('specialization', '').strip().lower()

    # Query active team members with optimized relational joins
    members_qs = TeamMember.objects.select_related('department').prefetch_related('specializations').all()

    # Apply keyword search across multiple textual attributes
    if search_query:
        members_qs = members_qs.filter(
            Q(name__icontains=search_query) |
            Q(role__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(skills__icontains=search_query) |
            Q(department__name__icontains=search_query) |
            Q(department_name__icontains=search_query) |
            Q(specializations__name__icontains=search_query)
        ).distinct()

    # Apply department filtering
    if dept_slug and dept_slug != 'all':
        members_qs = members_qs.filter(
            Q(department__slug=dept_slug) | Q(department_slug=dept_slug)
        )

    # Apply specialization filtering
    if spec_slug and spec_slug != 'all':
        members_qs = members_qs.filter(
            specializations__slug=spec_slug
        ).distinct()

    members = list(members_qs)

    # Fetch filter options for tabs and dropdowns
    departments = Department.objects.all()
    specializations = Specialization.objects.select_related('department').all()

    all_members_count = TeamMember.objects.count()
    total_departments = departments.count()
    total_specializations = specializations.count()

    # Partition into leadership and specialists
    leadership = [m for m in members if m.is_leadership]
    specialists = [m for m in members if not m.is_leadership]

    return render(request, 'teams/index.html', {
        'members': members,
        'leadership': leadership,
        'specialists': specialists,
        'departments': departments,
        'specializations': specializations,
        'current_department': dept_slug or 'all',
        'current_specialization': spec_slug or 'all',
        'search_query': search_query,
        'total_results': len(members),
        'all_members_count': all_members_count,
        'total_departments': total_departments,
        'total_specializations': total_specializations,
    })


def team_detail(request, pk):
    """
    Render a comprehensive profile page for a single team member.

    Displays technical credentials, biographic narrative, specialization tags,
    social profiles, and external portfolio site links.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the requested TeamMember.

    Returns:
        HttpResponse: Rendered member detail page.
    """
    member = get_object_or_404(
        TeamMember.objects.select_related('department').prefetch_related('specializations'),
        pk=pk
    )
    # Fetch related colleagues for discovery recommendations
    other_members = TeamMember.objects.exclude(pk=member.pk).select_related('department')[:4]

    return render(request, 'teams/detail.html', {
        'member': member,
        'other_members': other_members,
    })
