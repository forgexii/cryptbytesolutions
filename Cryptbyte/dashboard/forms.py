from django import forms
from blogs.models import BlogPost, BlogCategory
from solutions.models import Solution
from projects.models import Project
from teams.models import TeamMember, Department, Specialization


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title', 'slug', 'category', 'category_name', 'author', 'author_role',
            'author_avatar', 'read_time', 'published_date', 'image', 'is_featured',
            'is_published', 'tags', 'excerpt', 'content'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter blog article title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. distributed-ai-microservices'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'category_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. AI & Machine Learning'}),
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Marcus Vance'}),
            'author_role': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Chief Technology Officer'}),
            'author_avatar': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Initials, e.g. MV'}),
            'read_time': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 5 min read'}),
            'published_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'tags': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Comma-separated: Architecture, AI, Cloud'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Short summary for card previews'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 12, 'placeholder': 'Full article content (supports HTML)'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = [
            'title', 'slug', 'category', 'tagline', 'short_desc', 'icon_type',
            'image', 'overview', 'metrics_json', 'challenges_json', 'capabilities_json',
            'roadmap_json', 'technologies', 'timeline', 'delivery_model',
            'target_industries', 'deployment', 'compliance', 'order', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Business Process Automation'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. business-process-automation'}),
            'category': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Enterprise, Security, Commerce'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'High-impact value proposition sentence'}),
            'short_desc': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Card preview description'}),
            'icon_type': forms.Select(attrs={'class': 'form-select'}),
            'overview': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8, 'placeholder': 'Deep dive overview of the solution'}),
            'technologies': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Comma-separated: Python, Celery, Redis, Docker'}),
            'timeline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 3 to 6 weeks'}),
            'delivery_model': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Agile sprints with bi-weekly demos'}),
            'target_industries': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Finance, Logistics, Real Estate'}),
            'deployment': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Cloud-native, Dedicated VPC, or Hybrid'}),
            'compliance': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. SOC 2 Type II and GDPR compliant'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'metrics_json': forms.Textarea(attrs={'class': 'form-textarea code-font', 'rows': 4, 'placeholder': '[{"value": "85%", "label": "Manual Effort Cut", "desc": "Reduction in hours"}]'}),
            'challenges_json': forms.Textarea(attrs={'class': 'form-textarea code-font', 'rows': 5, 'placeholder': '[{"problem": "Data Silos", "problem_desc": "...", "solution": "API Orchestration", "solution_desc": "..."}]'}),
            'capabilities_json': forms.Textarea(attrs={'class': 'form-textarea code-font', 'rows': 5, 'placeholder': '[{"title": "Event Orchestration", "desc": "..."}]'}),
            'roadmap_json': forms.Textarea(attrs={'class': 'form-textarea code-font', 'rows': 4, 'placeholder': '[{"step": "01", "phase": "Discovery", "summary": "..."}]'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'category', 'tagline', 'description', 'image',
            'stack', 'live_url', 'github_url', 'order', 'is_featured', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. SecureNet: Threat Intelligence Platform'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. securenet-threat-intelligence'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Short summary or client description'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Detailed case study or project explanation'}),
            'stack': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Comma-separated: Python, Django, React, Docker'}),
            'live_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://example.com'}),
            'github_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/...'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            'name', 'role', 'department', 'department_name', 'specializations',
            'bio', 'initials', 'skills', 'image', 'linkedin_url', 'github_url',
            'twitter_url', 'order', 'is_leadership'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Alex Chen'}),
            'role': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Principal Systems Architect'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'department_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Custom department label if needed'}),
            'specializations': forms.SelectMultiple(attrs={'class': 'form-select form-select--multiple', 'size': 5}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Background, credentials, and expertise narrative'}),
            'initials': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. AC (auto-calculated if blank)'}),
            'skills': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Comma-separated tags: Distributed Systems, Go, Python'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://linkedin.com/in/...'}),
            'github_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/...'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://x.com/...'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_leadership': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'slug', 'description', 'order', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Systems Engineering'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. systems-engineering'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Department core focus and mandate'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name', 'slug', 'department', 'description', 'order', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Distributed Systems'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. distributed-systems'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Specific technical competencies and domain focus'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }

