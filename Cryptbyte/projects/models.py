from django.db import models


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web App'),
        ('ai', 'AI / ML'),
        ('cloud', 'Cloud'),
        ('security', 'Security'),
    ]

    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='web', null=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True, null=True, help_text="Short subtitle or client name")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    stack = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated technologies")
    live_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, null=True, blank=True)
    is_featured = models.BooleanField(default=False, null=True, blank=True)
    is_published = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-is_featured', 'order', 'title']

    def __str__(self):
        cat = self.get_category_display() if hasattr(self, 'get_category_display') else self.category
        title = self.title or "Untitled Project"
        if cat:
            return f"{title} ({cat})"
        return title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            from django.utils.text import slugify
            base_slug = slugify(self.title) or 'project'
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def stack_list(self):
        if not self.stack:
            return []
        return [s.strip() for s in self.stack.split(',') if s.strip()]

    @property
    def category_icon(self):
        icons = {
            'web': '🌐',
            'ai': '🤖',
            'cloud': '☁️',
            'security': '🔒',
        }
        return icons.get(self.category, '💼')
