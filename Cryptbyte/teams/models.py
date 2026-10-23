"""
Cryptbyte Solutions - Teams Data Models

Defines the organizational hierarchy and member profiles:
- Department: Top-level organizational unit (e.g. Engineering, AI Research, Cyber Defense).
- Specialization: Technical domain or focus area nested within a department.
- TeamMember: Staff profile containing roles, skills, social links, and portfolio references.
"""

from django.db import models
from Cryptbyte.utils import generate_unique_slug, generate_initials, split_comma_string


class Department(models.Model):
    """
    Top-level organizational department within Cryptbyte Solutions.

    Groups specialized talent and provides filtering categories on public teams pages.
    """
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='departments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name or "Unnamed Department"

    def save(self, *args, **kwargs):
        """Auto-populate slug from department name on initial persistence."""
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self, self.name, fallback='department')
        super().save(*args, **kwargs)

    @property
    def member_count(self):
        """Total count of team members assigned to this department."""
        return self.members.count()


class Specialization(models.Model):
    """
    Specific technical discipline or focus area nested within a department.

    Assigned to team members to highlight granular technical capabilities.
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='specializations',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='specializations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        if self.department and self.department.name:
            return f"{self.name or 'Specialization'} ({self.department.name})"
        return self.name or "Unnamed Specialization"

    def save(self, *args, **kwargs):
        """Auto-populate slug from specialization name on initial persistence."""
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self, self.name, fallback='specialization')
        super().save(*args, **kwargs)


class TeamMember(models.Model):
    """
    Professional profile of an individual engineer, researcher, or leadership member.

    Contains personal bio, department affiliations, multi-discipline specializations,
    skill tags, social profiles, and external portfolio URLs.
    """
    name = models.CharField(max_length=120, null=True, blank=True)
    role = models.CharField(max_length=120, null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    department_name = models.CharField(max_length=100, blank=True, null=True)
    department_slug = models.SlugField(max_length=80, blank=True, null=True)
    specializations = models.ManyToManyField(
        Specialization,
        blank=True,
        related_name='members'
    )
    bio = models.TextField(blank=True, null=True)
    initials = models.CharField(max_length=5, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated skill tags")
    image = models.ImageField(upload_to='teams/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True, help_text="Personal or professional portfolio website URL")
    order = models.PositiveIntegerField(default=0, null=True, blank=True)
    is_leadership = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        dept = self.department.name if (self.department and self.department.name) else self.department_name
        name = self.name or "Unnamed Member"
        role = self.role or "Member"
        if dept:
            return f"{name} - {role} ({dept})"
        return f"{name} - {role}"

    def save(self, *args, **kwargs):
        """Auto-populate department snapshots and avatar initials on save."""
        if self.department:
            if self.department.name:
                self.department_name = self.department.name
            if self.department.slug:
                self.department_slug = self.department.slug
        if not self.initials and self.name:
            self.initials = generate_initials(self.name)
        super().save(*args, **kwargs)

    @property
    def display_department(self):
        """Human-readable department name with fallback."""
        if self.department and self.department.name:
            return self.department.name
        return self.department_name or "General"

    @property
    def skill_list(self):
        """Parse comma-separated skills string into a list of clean tokens."""
        return split_comma_string(self.skills)

    @property
    def specialization_list(self):
        """List of active Specialization objects associated with this member."""
        return list(self.specializations.all())

    @property
    def linkedin(self):
        """Convenience alias for linkedin_url."""
        return self.linkedin_url

    @property
    def github(self):
        """Convenience alias for github_url."""
        return self.github_url

    @property
    def twitter(self):
        """Convenience alias for twitter_url."""
        return self.twitter_url

    @property
    def portfolio(self):
        """Convenience alias for portfolio_url."""
        return self.portfolio_url
