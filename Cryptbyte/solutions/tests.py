"""
Cryptbyte Solutions - Solutions Application Tests
"""

from django.test import TestCase
from django.urls import reverse
from .models import Solution


class SolutionsViewTestCase(TestCase):
    """Verifies that the solutions catalog and detail views render successfully."""

    def setUp(self):
        """Seed a sample solution record."""
        self.solution = Solution.objects.create(
            title="Enterprise Cloud Migration",
            slug="enterprise-cloud-migration",
            is_published=True,
        )

    def test_solutions_index_page(self):
        """Ensure solutions catalog responds with HTTP 200 OK."""
        response = self.client.get(reverse('solutions:solutions'))
        self.assertEqual(response.status_code, 200)

    def test_solution_detail_page(self):
        """Ensure solution case study responds with HTTP 200 OK."""
        response = self.client.get(reverse('solutions:solution_detail', kwargs={'slug': self.solution.slug}))
        self.assertEqual(response.status_code, 200)
