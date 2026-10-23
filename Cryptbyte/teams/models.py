from django.db import models
from Cryptbyte.utils import generate_unique_slug, generate_initials, split_comma_string


class Department(models.Model):
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
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self, self.name, fallback='department')
        super().save(*args, **kwargs)

    @property
    def member_count(self):
        return self.members.count()


class Specialization(models.Model):
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
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self, self.name, fallback='specialization')
        super().save(*args, **kwargs)


class TeamMember(models.Model):
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
        if self.department and self.department.name:
            return self.department.name
        return self.department_name or "General"

    @property
    def skill_list(self):
        return split_comma_string(self.skills)

    @property
    def specialization_list(self):
        return list(self.specializations.all())

    @property
    def linkedin(self):
        return self.linkedin_url

    @property
    def github(self):
        return self.github_url

    @property
    def twitter(self):
        return self.twitter_url

    @property
    def portfolio(self):
        return self.portfolio_url
