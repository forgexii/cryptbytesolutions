from django.db import models


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
            from django.utils.text import slugify
            base_slug = slugify(self.name) or 'department'
            slug = base_slug
            counter = 1
            while Department.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
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
            from django.utils.text import slugify
            base_slug = slugify(self.name) or 'specialization'
            slug = base_slug
            counter = 1
            while Specialization.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
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
            parts = self.name.strip().split()
            if len(parts) >= 2:
                self.initials = (parts[0][0] + parts[-1][0]).upper()
            elif parts:
                self.initials = parts[0][:2].upper()
        super().save(*args, **kwargs)

    @property
    def display_department(self):
        if self.department and self.department.name:
            return self.department.name
        return self.department_name or "General"

    @property
    def skill_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def specialization_list(self):
        return list(self.specializations.all())
