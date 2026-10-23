"""
Cryptbyte Solutions - Staff Administration Dashboard Views

Provides authenticated administrative endpoints for the internal management portal:
- Authentication: Secure login, open-redirect protection, and session termination.
- Overview: Real-time firm KPIs, publishing metrics, and recent activity streams.
- Blogs CRUD: Article authoring, draft toggling, editing, and deletion.
- Solutions CRUD: Enterprise product solutions, JSON metrics/roadmaps management.
- Projects CRUD: Flagship case studies, technology stacks, and live links management.
- Teams CRUD: Personnel directory, roles, leadership designation, and portfolio links.
- Departments & Specializations CRUD: Corporate hierarchy and technical focus management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Q

from blogs.models import BlogPost
from solutions.models import Solution
from projects.models import Project
from teams.models import TeamMember, Department, Specialization

from .forms import (
    BlogPostForm,
    SolutionForm,
    ProjectForm,
    TeamMemberForm,
    DepartmentForm,
    SpecializationForm,
)


def is_staff(user):
    """
    Check whether a user is authenticated and holds active staff permissions.

    Args:
        user (User): The request user to inspect.

    Returns:
        bool: True if user is authenticated and is_staff is True, else False.
    """
    return user.is_authenticated and user.is_staff


def staff_member_required(view_func):
    """
    View decorator requiring user authentication and active staff permissions.

    Redirects unauthorized or unauthenticated users to the dashboard login page.
    """
    return user_passes_test(is_staff, login_url='dashboard:login')(view_func)


# ========================================================
# AUTHENTICATION
# ========================================================
def dashboard_login(request):
    """
    Staff login view for authenticating internal administrators into the dashboard.

    Security features:
    - Restricts dashboard entry strictly to users with is_staff=True.
    - Validates target redirect URLs using url_has_allowed_host_and_scheme to prevent open redirects.
    - Configures configurable session expiry (2 weeks for Remember Me, browser session otherwise).

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered login page or HTTP redirect on successful authentication.
    """
    # If user is already authenticated with staff rights, skip login
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:home')

    error_message = None
    info_message = None
    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.user.is_authenticated and not request.user.is_staff:
        error_message = "Access restricted: Your account does not have staff permissions for the Cryptbyte dashboard."
    elif request.GET.get('next') and not request.user.is_authenticated:
        info_message = "Authentication required: Please enter your staff credentials to proceed."

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            error_message = "Please provide both your username and password."
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    # Configure session persistence
                    if remember_me:
                        request.session.set_expiry(1209600)  # 14 days
                    else:
                        request.session.set_expiry(0)  # Browser session closure

                    # Defend against open redirects
                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect('dashboard:home')
                else:
                    error_message = "Access restricted: This account does not possess staff privileges required to access the dashboard."
            else:
                error_message = "Invalid username or password. Please verify your credentials and try again."

    return render(request, 'dashboard/login.html', {
        'error_message': error_message,
        'info_message': info_message,
        'next': next_url,
    })


def dashboard_logout(request):
    """
    Terminate staff administrative session and clear session credentials.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponseRedirect: Redirect to dashboard login with confirmation flash.
    """
    logout(request)
    messages.info(request, "You have been logged out securely.")
    return redirect('dashboard:login')


# ========================================================
# DASHBOARD OVERVIEW
# ========================================================
@staff_member_required
def dashboard_home(request):
    """
    Render administrative overview dashboard with aggregate metrics and recent records.

    Summarizes live database figures across blogs, solutions, projects, teams,
    and feeds recent items to speed up editorial and content updates.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered dashboard overview template with stats and activity feeds.
    """
    # Aggregate counts across all entities
    total_blogs = BlogPost.objects.count()
    published_blogs = BlogPost.objects.filter(is_published=True).count()
    draft_blogs = total_blogs - published_blogs

    total_solutions = Solution.objects.count()
    published_solutions = Solution.objects.filter(is_published=True).count()

    total_projects = Project.objects.count()
    featured_projects = Project.objects.filter(is_featured=True).count()

    total_teams = TeamMember.objects.count()
    total_depts = Department.objects.count()
    total_specs = Specialization.objects.count()

    # Recent activity queries
    recent_blogs = BlogPost.objects.order_by('-created_at')[:5]
    recent_solutions = Solution.objects.order_by('-created_at')[:5]
    recent_projects = Project.objects.order_by('-created_at')[:5]
    recent_teams = TeamMember.objects.select_related('department').order_by('-created_at')[:5]

    return render(request, 'dashboard/index.html', {
        'page_title': 'Dashboard Overview',
        'active_tab': 'overview',
        'stats': {
            'blogs': {'total': total_blogs, 'published': published_blogs, 'drafts': draft_blogs},
            'solutions': {'total': total_solutions, 'published': published_solutions},
            'projects': {'total': total_projects, 'featured': featured_projects},
            'teams': {'total': total_teams, 'departments': total_depts, 'specializations': total_specs},
        },
        'recent_blogs': recent_blogs,
        'recent_solutions': recent_solutions,
        'recent_projects': recent_projects,
        'recent_teams': recent_teams,
    })


# ========================================================
# BLOGS CRUD
# ========================================================
@staff_member_required
def blog_list(request):
    """
    List and filter engineering blog articles in the administration portal.

    Supports keyword search and status filtering (published vs draft).

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered blog articles management table.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip().lower()

    posts = BlogPost.objects.select_related('category').all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category_name__icontains=query) |
            Q(tags__icontains=query)
        )

    if status_filter == 'published':
        posts = posts.filter(is_published=True)
    elif status_filter == 'draft':
        posts = posts.filter(is_published=False)

    return render(request, 'dashboard/blogs/list.html', {
        'page_title': 'Blog Articles',
        'active_tab': 'blogs',
        'posts': posts,
        'search_query': query,
        'status_filter': status_filter or 'all',
        'total_count': posts.count(),
    })


@staff_member_required
def blog_create(request):
    """
    Handle creation and publishing of a new blog article.

    Processes file uploads and enforces title, category, and content validations.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered form template or redirect to blog list on creation.
    """
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Blog post "{post.title}" was published successfully.')
            return redirect('dashboard:blog_list')
    else:
        form = BlogPostForm()

    return render(request, 'dashboard/blogs/form.html', {
        'page_title': 'Publish New Blog Post',
        'active_tab': 'blogs',
        'form': form,
        'is_edit': False,
    })


@staff_member_required
def blog_edit(request, pk):
    """
    Edit an existing blog article and update associated media or tags.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the BlogPost to modify.

    Returns:
        HttpResponse: Rendered edit form template or redirect on successful update.
    """
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Blog post "{post.title}" was updated.')
            return redirect('dashboard:blog_list')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'dashboard/blogs/form.html', {
        'page_title': f'Edit Article: {post.title}',
        'active_tab': 'blogs',
        'form': form,
        'post': post,
        'is_edit': True,
    })


@staff_member_required
def blog_delete(request, pk):
    """
    Prompt confirmation and handle permanent deletion of a blog article.

    Requires POST submission to perform the deletion side effect.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the BlogPost to delete.

    Returns:
        HttpResponse: Rendered delete confirmation template or redirect on deletion.
    """
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Blog post "{title}" was deleted.')
        return redirect('dashboard:blog_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'page_title': 'Confirm Delete Blog Post',
        'active_tab': 'blogs',
        'object_name': post.title,
        'object_type': 'Blog Post',
        'cancel_url': 'dashboard:blog_list',
    })


@staff_member_required
def blog_toggle_publish(request, pk):
    """
    Quickly toggle the publication state (published vs draft) of a blog article.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the BlogPost.

    Returns:
        HttpResponseRedirect: Redirect back to blog articles list with confirmation.
    """
    post = get_object_or_404(BlogPost, pk=pk)
    post.is_published = not post.is_published
    post.save()
    status_text = 'published' if post.is_published else 'moved to drafts'
    messages.info(request, f'"{post.title}" is now {status_text}.')
    return redirect('dashboard:blog_list')


# ========================================================
# SOLUTIONS CRUD
# ========================================================
@staff_member_required
def solution_list(request):
    """
    List, search, and manage enterprise solutions in the admin panel.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered solutions management table.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip().lower()

    solutions_qs = Solution.objects.all()

    if query:
        solutions_qs = solutions_qs.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(tagline__icontains=query) |
            Q(technologies__icontains=query)
        )

    if status_filter == 'published':
        solutions_qs = solutions_qs.filter(is_published=True)
    elif status_filter == 'draft':
        solutions_qs = solutions_qs.filter(is_published=False)

    return render(request, 'dashboard/solutions/list.html', {
        'page_title': 'Solutions Management',
        'active_tab': 'solutions',
        'solutions': solutions_qs,
        'search_query': query,
        'status_filter': status_filter or 'all',
        'total_count': solutions_qs.count(),
    })


@staff_member_required
def solution_create(request):
    """
    Create a new product solution with specifications and JSON payloads.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered solution creation form or redirect on save.
    """
    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            solution = form.save()
            messages.success(request, f'Solution "{solution.title}" was created successfully.')
            return redirect('dashboard:solution_list')
    else:
        form = SolutionForm()

    return render(request, 'dashboard/solutions/form.html', {
        'page_title': 'Add New Solution',
        'active_tab': 'solutions',
        'form': form,
        'is_edit': False,
    })


@staff_member_required
def solution_edit(request, pk):
    """
    Modify an existing Solution record, roadmap, metrics, or delivery specs.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Solution.

    Returns:
        HttpResponse: Rendered solution edit form or redirect on save.
    """
    solution = get_object_or_404(Solution, pk=pk)
    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES, instance=solution)
        if form.is_valid():
            solution = form.save()
            messages.success(request, f'Solution "{solution.title}" was updated.')
            return redirect('dashboard:solution_list')
    else:
        form = SolutionForm(instance=solution)

    return render(request, 'dashboard/solutions/form.html', {
        'page_title': f'Edit Solution: {solution.title}',
        'active_tab': 'solutions',
        'form': form,
        'solution': solution,
        'is_edit': True,
    })


@staff_member_required
def solution_delete(request, pk):
    """
    Prompt confirmation and permanently delete a Solution offering.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Solution.

    Returns:
        HttpResponse: Rendered confirmation template or redirect on deletion.
    """
    solution = get_object_or_404(Solution, pk=pk)
    if request.method == 'POST':
        title = solution.title
        solution.delete()
        messages.success(request, f'Solution "{title}" was removed.')
        return redirect('dashboard:solution_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'page_title': 'Confirm Delete Solution',
        'active_tab': 'solutions',
        'object_name': solution.title,
        'object_type': 'Solution',
        'cancel_url': 'dashboard:solution_list',
    })


@staff_member_required
def solution_toggle_publish(request, pk):
    """
    Toggle active publication visibility for a Solution offering.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Solution.

    Returns:
        HttpResponseRedirect: Redirect back to solutions list with confirmation.
    """
    solution = get_object_or_404(Solution, pk=pk)
    solution.is_published = not solution.is_published
    solution.save()
    status_text = 'active' if solution.is_published else 'hidden'
    messages.info(request, f'Solution "{solution.title}" is now {status_text}.')
    return redirect('dashboard:solution_list')


# ========================================================
# PROJECTS CRUD
# ========================================================
@staff_member_required
def project_list(request):
    """
    List and filter engineering portfolio projects in the admin panel.

    Supports keyword search across titles, descriptions, and stacks, as well as category filtering.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered project management table.
    """
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip().lower()

    projects_qs = Project.objects.all()

    if query:
        projects_qs = projects_qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(stack__icontains=query) |
            Q(tagline__icontains=query)
        )

    if category_filter and category_filter != 'all':
        projects_qs = projects_qs.filter(category=category_filter)

    return render(request, 'dashboard/projects/list.html', {
        'page_title': 'Projects Portfolio',
        'active_tab': 'projects',
        'projects': projects_qs,
        'search_query': query,
        'category_filter': category_filter or 'all',
        'categories': Project.CATEGORY_CHOICES,
        'total_count': projects_qs.count(),
    })


@staff_member_required
def project_create(request):
    """
    Create a new portfolio case study with stack tags and demonstration links.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered project creation form or redirect on save.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.title}" was added.')
            return redirect('dashboard:project_list')
    else:
        form = ProjectForm()

    return render(request, 'dashboard/projects/form.html', {
        'page_title': 'Add New Project',
        'active_tab': 'projects',
        'form': form,
        'is_edit': False,
    })


@staff_member_required
def project_edit(request, pk):
    """
    Edit an existing portfolio case study, featured status, or technology stack.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Project.

    Returns:
        HttpResponse: Rendered project edit form or redirect on save.
    """
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.title}" was updated.')
            return redirect('dashboard:project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'dashboard/projects/form.html', {
        'page_title': f'Edit Project: {project.title}',
        'active_tab': 'projects',
        'form': form,
        'project': project,
        'is_edit': True,
    })


@staff_member_required
def project_delete(request, pk):
    """
    Prompt confirmation and permanently delete a portfolio case study.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Project.

    Returns:
        HttpResponse: Rendered confirmation template or redirect on deletion.
    """
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" was deleted.')
        return redirect('dashboard:project_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'page_title': 'Confirm Delete Project',
        'active_tab': 'projects',
        'object_name': project.title,
        'object_type': 'Project',
        'cancel_url': 'dashboard:project_list',
    })


@staff_member_required
def project_toggle_publish(request, pk):
    """
    Toggle visibility status (published vs hidden) for a portfolio item.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Project.

    Returns:
        HttpResponseRedirect: Redirect back to projects list with confirmation.
    """
    project = get_object_or_404(Project, pk=pk)
    project.is_published = not project.is_published
    project.save()
    status_text = 'published' if project.is_published else 'hidden'
    messages.info(request, f'Project "{project.title}" is now {status_text}.')
    return redirect('dashboard:project_list')


# ========================================================
# TEAMS CRUD
# ========================================================
@staff_member_required
def team_list(request):
    """
    Manage team members, roles, department affiliations, and specializations.

    Supports keyword search across names, roles, skills, and department/specialization filters.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered team directory management table.
    """
    query = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('department', '').strip().lower()
    spec_filter = request.GET.get('specialization', '').strip().lower()

    members_qs = TeamMember.objects.select_related('department').prefetch_related('specializations').all()

    if query:
        members_qs = members_qs.filter(
            Q(name__icontains=query) |
            Q(role__icontains=query) |
            Q(skills__icontains=query) |
            Q(department__name__icontains=query) |
            Q(specializations__name__icontains=query)
        ).distinct()

    if dept_filter and dept_filter != 'all':
        members_qs = members_qs.filter(
            Q(department__slug=dept_filter) | Q(department_slug=dept_filter)
        )

    if spec_filter and spec_filter != 'all':
        members_qs = members_qs.filter(
            specializations__slug=spec_filter
        ).distinct()

    departments = Department.objects.all()
    specializations = Specialization.objects.select_related('department').all()

    return render(request, 'dashboard/teams/list.html', {
        'page_title': 'Team Members',
        'active_tab': 'teams',
        'members': members_qs,
        'departments': departments,
        'specializations': specializations,
        'search_query': query,
        'dept_filter': dept_filter or 'all',
        'spec_filter': spec_filter or 'all',
        'total_count': members_qs.count(),
    })


@staff_member_required
def team_create(request):
    """
    Add a new team member with skills, credentials, and optional portfolio website URL.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered member creation form or redirect on save.
    """
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'Team member "{member.name}" was added successfully.')
            return redirect('dashboard:team_list')
    else:
        form = TeamMemberForm()

    return render(request, 'dashboard/teams/form.html', {
        'page_title': 'Add Team Member',
        'active_tab': 'teams',
        'form': form,
        'is_edit': False,
    })


@staff_member_required
def team_edit(request, pk):
    """
    Edit an existing team member profile, social links, or portfolio URL.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the TeamMember.

    Returns:
        HttpResponse: Rendered member edit form or redirect on save.
    """
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'Team member "{member.name}" was updated.')
            return redirect('dashboard:team_list')
    else:
        form = TeamMemberForm(instance=member)

    return render(request, 'dashboard/teams/form.html', {
        'page_title': f'Edit Team Member: {member.name}',
        'active_tab': 'teams',
        'form': form,
        'member': member,
        'is_edit': True,
    })


@staff_member_required
def team_delete(request, pk):
    """
    Prompt confirmation and permanently delete a team member profile.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the TeamMember.

    Returns:
        HttpResponse: Rendered confirmation template or redirect on deletion.
    """
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        name = member.name
        member.delete()
        messages.success(request, f'Team member "{name}" was removed.')
        return redirect('dashboard:team_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'page_title': 'Confirm Delete Team Member',
        'active_tab': 'teams',
        'object_name': member.name,
        'object_type': 'Team Member',
        'cancel_url': 'dashboard:team_list',
    })


# ========================================================
# DEPARTMENTS & SPECIALIZATIONS CRUD
# ========================================================
@staff_member_required
def department_list(request):
    """
    View all corporate organizational departments and nested specializations.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered departments and specializations overview.
    """
    departments = Department.objects.prefetch_related('specializations', 'members').all()
    specializations = Specialization.objects.select_related('department').all()

    return render(request, 'dashboard/departments/list.html', {
        'page_title': 'Departments & Specializations',
        'active_tab': 'departments',
        'departments': departments,
        'specializations': specializations,
    })


@staff_member_required
def department_create(request):
    """
    Create a new organizational department.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered department creation form or redirect on save.
    """
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" was created.')
            return redirect('dashboard:department_list')
    else:
        form = DepartmentForm()

    return render(request, 'dashboard/departments/form.html', {
        'page_title': 'Create Department',
        'active_tab': 'departments',
        'form': form,
        'is_edit': False,
        'type': 'Department',
    })


@staff_member_required
def department_edit(request, pk):
    """
    Edit an existing department name, slug, or focus mandate.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Department.

    Returns:
        HttpResponse: Rendered department edit form or redirect on save.
    """
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=dept)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" was updated.')
            return redirect('dashboard:department_list')
    else:
        form = DepartmentForm(instance=dept)

    return render(request, 'dashboard/departments/form.html', {
        'page_title': f'Edit Department: {dept.name}',
        'active_tab': 'departments',
        'form': form,
        'is_edit': True,
        'type': 'Department',
    })


@staff_member_required
def department_delete(request, pk):
    """
    Prompt confirmation and permanently delete an organizational department.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Department.

    Returns:
        HttpResponse: Rendered confirmation template or redirect on deletion.
    """
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        name = dept.name
        dept.delete()
        messages.success(request, f'Department "{name}" was deleted.')
        return redirect('dashboard:department_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'page_title': 'Confirm Delete Department',
        'active_tab': 'departments',
        'object_name': dept.name,
        'object_type': 'Department',
        'cancel_url': 'dashboard:department_list',
    })


@staff_member_required
def specialization_create(request):
    """
    Create a new technical discipline associated with a parent department.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered specialization creation form or redirect on save.
    """
    if request.method == 'POST':
        form = SpecializationForm(request.POST, request.FILES)
        if form.is_valid():
            spec = form.save()
            messages.success(request, f'Specialization "{spec.name}" was created.')
            return redirect('dashboard:department_list')
    else:
        form = SpecializationForm()

    return render(request, 'dashboard/departments/form.html', {
        'page_title': 'Create Specialization',
        'active_tab': 'departments',
        'form': form,
        'is_edit': False,
        'type': 'Specialization',
    })


@staff_member_required
def specialization_edit(request, pk):
    """
    Edit an existing specialization and its parent department mapping.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Specialization.

    Returns:
        HttpResponse: Rendered specialization edit form or redirect on save.
    """
    spec = get_object_or_404(Specialization, pk=pk)
    if request.method == 'POST':
        form = SpecializationForm(request.POST, request.FILES, instance=spec)
        if form.is_valid():
            spec = form.save()
            messages.success(request, f'Specialization "{spec.name}" was updated.')
            return redirect('dashboard:department_list')
    else:
        form = SpecializationForm(instance=spec)

    return render(request, 'dashboard/departments/form.html', {
        'page_title': f'Edit Specialization: {spec.name}',
        'active_tab': 'departments',
        'form': form,
        'is_edit': True,
        'type': 'Specialization',
    })


@staff_member_required
def specialization_delete(request, pk):
    """
    Prompt confirmation and permanently delete a technical specialization.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        pk (int): Primary key ID of the Specialization.

    Returns:
        HttpResponse: Rendered confirmation template or redirect on deletion.
    """
    spec = get_object_or_404(Specialization, pk=pk)
    if request.method == 'POST':
        name = spec.name
        spec.delete()
        messages.success(request, f'Specialization "{name}" was deleted.')
        return redirect('dashboard:department_list')

    return render(request, 'dashboard/confirm_delete.html', {
        'page_title': 'Confirm Delete Specialization',
        'active_tab': 'departments',
        'object_name': spec.name,
        'object_type': 'Specialization',
        'cancel_url': 'dashboard:department_list',
    })
