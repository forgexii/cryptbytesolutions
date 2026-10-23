"""
Cryptbyte Solutions - Dashboard Administration Forms

Provides validated ModelForms for staff content management:
- BlogPostForm: Authoring, editing, and publishing articles with rich content.
- SolutionForm: Enterprise solutions with structured JSON payloads and metrics.
- ProjectForm: Flagship engineering case studies, tech stacks, and live links.
- TeamMemberForm: Staff profiles, leadership designations, and external portfolios.
- DepartmentForm: Top-level organizational divisions and focus mandates.
- SpecializationForm: Granular technical disciplines within departments.

Includes defense-in-depth security validations:
- Image file size restrictions (10 MB maximum).
- JSON array structure and syntax verification.
"""

import json
from django import forms
from django.core.exceptions import ValidationError
from blogs.models import BlogPost
from solutions.models import Solution
from projects.models import Project
from teams.models import TeamMember, Department, Specialization

MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit to prevent resource exhaustion


def validate_image_upload(image):
    """
    Ensure uploaded image file sizes do not exceed safe operational thresholds.

    Guards against denial-of-service attempts via oversized media uploads.

    Args:
        image (UploadedFile): The uploaded file instance.

    Returns:
        UploadedFile: The validated image file.

    Raises:
        ValidationError: If the uploaded file exceeds 10 MB.
    """
    if not image or not hasattr(image, 'size'):
        return image
    if image.size > MAX_UPLOAD_SIZE_BYTES:
        raise ValidationError("Image file size must not exceed 10 MB.")
    return image


def validate_json_array(value, field_label):
    """
    Validate that user-submitted text contains well-formed JSON array syntax.

    Args:
        value (str): Raw JSON string input from the form textarea.
        field_label (str): Human-readable name of the field for error reporting.

    Returns:
        str: Validated JSON string.

    Raises:
        ValidationError: If JSON is invalid or deserializes into a non-list object.
    """
    if not value or not str(value).strip():
        return '[]'
    try:
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise ValidationError(f"{field_label} must be a valid JSON array format.")
        return value
    except (json.JSONDecodeError, ValueError):
        raise ValidationError(f"{field_label} contains invalid JSON syntax.")


class BlogPostForm(forms.ModelForm):
    """Staff administration form for drafting, authoring, and publishing blog articles."""
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

    def clean_image(self):
        """Validate image upload size."""
        return validate_image_upload(self.cleaned_data.get('image'))


class SolutionForm(forms.ModelForm):
    """Staff administration form for configuring enterprise solutions and JSON roadmaps."""
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

    def clean_image(self):
        """Validate image upload size."""
        return validate_image_upload(self.cleaned_data.get('image'))

    def clean_metrics_json(self):
        """Validate metrics JSON structure."""
        return validate_json_array(self.cleaned_data.get('metrics_json'), 'Metrics JSON')

    def clean_challenges_json(self):
        """Validate challenges JSON structure."""
        return validate_json_array(self.cleaned_data.get('challenges_json'), 'Challenges JSON')

    def clean_capabilities_json(self):
        """Validate capabilities JSON structure."""
        return validate_json_array(self.cleaned_data.get('capabilities_json'), 'Capabilities JSON')

    def clean_roadmap_json(self):
        """Validate roadmap JSON structure."""
        return validate_json_array(self.cleaned_data.get('roadmap_json'), 'Roadmap JSON')


class ProjectForm(forms.ModelForm):
    """Staff administration form for publishing portfolio case studies and tech stacks."""
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

    def clean_image(self):
        """Validate image upload size."""
        return validate_image_upload(self.cleaned_data.get('image'))


class TeamMemberForm(forms.ModelForm):
    """Staff administration form for registering personnel profiles and portfolio links."""
    class Meta:
        model = TeamMember
        fields = [
            'name', 'role', 'department', 'department_name', 'specializations',
            'bio', 'initials', 'skills', 'image', 'linkedin_url', 'github_url',
            'twitter_url', 'portfolio_url', 'order', 'is_leadership'
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
            'portfolio_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://yourportfolio.com'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'is_leadership': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean_image(self):
        """Validate image upload size."""
        return validate_image_upload(self.cleaned_data.get('image'))


class DepartmentForm(forms.ModelForm):
    """Staff administration form for managing corporate organizational departments."""
    class Meta:
        model = Department
        fields = ['name', 'slug', 'description', 'order', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Systems Engineering'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. systems-engineering'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Department core focus and mandate'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
        }

    def clean_image(self):
        """Validate image upload size."""
        return validate_image_upload(self.cleaned_data.get('image'))


class SpecializationForm(forms.ModelForm):
    """Staff administration form for managing technical disciplines within departments."""
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

    def clean_image(self):
        """Validate image upload size."""
        return validate_image_upload(self.cleaned_data.get('image'))

