from django.db import models
from django.utils import timezone
from Cryptbyte.utils import generate_unique_slug, generate_initials, split_comma_string


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blogs/categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name or "Unnamed Category"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(self, self.name, fallback='category')
        super().save(*args, **kwargs)

    @property
    def post_count(self):
        return self.posts.filter(is_published=True).count()


class BlogPost(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    category_name = models.CharField(max_length=100, default='Technology', null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, default='Cryptbyte Team', null=True, blank=True)
    author_role = models.CharField(max_length=100, default='Core Engineering', null=True, blank=True)
    author_avatar = models.CharField(max_length=10, blank=True, null=True, default='CB')
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    read_time = models.CharField(max_length=50, default='5 min read', null=True, blank=True)
    published_date = models.DateField(default=timezone.now, null=True, blank=True)
    is_featured = models.BooleanField(default=False, null=True, blank=True)
    is_published = models.BooleanField(default=True, null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-is_featured', '-published_date', '-created_at']

    def __str__(self):
        return self.title or "Untitled Blog Post"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = generate_unique_slug(self, self.title, fallback='post')
        if self.category and self.category.name:
            self.category_name = self.category.name
        if not self.author_avatar and self.author:
            self.author_avatar = generate_initials(self.author)
        super().save(*args, **kwargs)

    @property
    def tag_list(self):
        return split_comma_string(self.tags)

    @property
    def display_category(self):
        if self.category and self.category.name:
            return self.category.name
        return self.category_name or 'Engineering'
