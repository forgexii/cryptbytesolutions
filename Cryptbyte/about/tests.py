"""
Cryptbyte Solutions - About Application Tests
"""

from django.test import TestCase
from django.urls import reverse


class AboutViewTestCase(TestCase):
    """Verifies that the corporate about page renders successfully."""

    def test_about_page_status_code(self):
        """Ensure about page responds with HTTP 200 OK."""
        response = self.client.get(reverse('about:about'))
        self.assertEqual(response.status_code, 200)
