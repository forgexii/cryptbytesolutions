"""
Cryptbyte Solutions - Projects Application Tests
"""

from django.test import TestCase
from django.urls import reverse
from .models import Project


class ProjectsViewTestCase(TestCase):
    """Verifies that the project portfolio catalog and detail views render successfully."""

    def setUp(self):
        """Seed a sample project case study record."""
        self.project = Project.objects.create(
            title="SecureNet Cloud",
            slug="securenet-cloud",
            is_published=True,
        )

    def test_projects_index_page(self):
        """Ensure projects catalog responds with HTTP 200 OK."""
        response = self.client.get(reverse('projects:projects'))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_page(self):
        """Ensure project detail case study responds with HTTP 200 OK."""
        response = self.client.get(reverse('projects:project_detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
