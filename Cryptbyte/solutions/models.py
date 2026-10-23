from django.db import models
from Cryptbyte.utils import generate_unique_slug, parse_json_list, split_comma_string


class Solution(models.Model):
    ICON_CHOICES = [
        ('automation', 'Automation / Enterprise'),
        ('analytics', 'Analytics / Charts'),
        ('ai', 'AI / Brain'),
        ('security', 'Security / Shield'),
        ('commerce', 'Commerce / Storefront'),
        ('cloud', 'Cloud / Server'),
    ]

    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    category = models.CharField(max_length=100, default='Enterprise', null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    short_desc = models.TextField(null=True, blank=True)
    icon_type = models.CharField(max_length=50, choices=ICON_CHOICES, default='automation', null=True, blank=True)
    image = models.ImageField(upload_to='solutions/', blank=True, null=True)
    overview = models.TextField(null=True, blank=True)
    metrics_json = models.TextField(blank=True, null=True, default='[]', help_text="JSON list of {value, label, desc}")
    challenges_json = models.TextField(blank=True, null=True, default='[]', help_text="JSON list of {problem, problem_desc, solution, solution_desc}")
    capabilities_json = models.TextField(blank=True, null=True, default='[]', help_text="JSON list of {title, desc}")
    roadmap_json = models.TextField(blank=True, null=True, default='[]', help_text="JSON list of {step, phase, summary}")
    technologies = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated technologies")
    timeline = models.CharField(max_length=100, default='4 to 8 weeks', null=True, blank=True)
    delivery_model = models.CharField(max_length=255, default='Agile sprints with weekly demos', null=True, blank=True)
    target_industries = models.CharField(max_length=255, default='Finance, Healthcare, SaaS, Logistics', null=True, blank=True)
    deployment = models.CharField(max_length=255, default='Cloud-native, Dedicated VPC, or Hybrid', null=True, blank=True)
    compliance = models.CharField(max_length=255, default='SOC 2 Type II, ISO 27001, and GDPR aligned', null=True, blank=True)
    order = models.PositiveIntegerField(default=0, null=True, blank=True)
    is_published = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        title = self.title or "Untitled Solution"
        if self.category:
            return f"{title} ({self.category})"
        return title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = generate_unique_slug(self, self.title, fallback='solution')
        super().save(*args, **kwargs)

    def get_metrics(self):
        return parse_json_list(self.metrics_json)

    def get_challenges(self):
        return parse_json_list(self.challenges_json)

    def get_capabilities(self):
        return parse_json_list(self.capabilities_json)

    def get_roadmap(self):
        return parse_json_list(self.roadmap_json)

    @property
    def tech_list(self):
        return split_comma_string(self.technologies)

    @property
    def quick_facts(self):
        return {
            'timeline': self.timeline or '4 to 8 weeks',
            'delivery_model': self.delivery_model or 'Agile sprints with weekly demos',
            'target_industries': self.target_industries or 'Finance, Healthcare, SaaS, Logistics',
            'deployment': self.deployment or 'Cloud-native, Dedicated VPC, or Hybrid',
            'compliance': self.compliance or 'SOC 2 Type II, ISO 27001, and GDPR aligned',
        }
