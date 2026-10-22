from django.shortcuts import render
from django.db.models import Q
from .models import TeamMember, Department, Specialization


def team_list(request):
    """Public Teams overview with department filtering and keyword search."""
    search_query = request.GET.get('q', '').strip()
    dept_slug = request.GET.get('department', '').strip().lower()
    spec_slug = request.GET.get('specialization', '').strip().lower()

    # Query active team members from database
    members_qs = TeamMember.objects.select_related('department').prefetch_related('specializations').all()

    # Apply keyword search
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

    # Apply department filter
    if dept_slug and dept_slug != 'all':
        members_qs = members_qs.filter(
            Q(department__slug=dept_slug) | Q(department_slug=dept_slug)
        )

    # Apply specialization filter
    if spec_slug and spec_slug != 'all':
        members_qs = members_qs.filter(
            specializations__slug=spec_slug
        ).distinct()

    members = list(members_qs)

    # Departments and specializations for filter tabs and search dropdowns
    departments = Department.objects.all()
    specializations = Specialization.objects.select_related('department').all()

    all_members_count = TeamMember.objects.count()
    total_departments = departments.count()
    total_specializations = specializations.count()

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
