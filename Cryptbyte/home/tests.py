"""
Cryptbyte Solutions - Home Application Tests
"""

from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):
    """Verifies that the public home landing page renders successfully."""

    def test_home_page_status_code(self):
        """Ensure homepage responds with HTTP 200 OK."""
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
