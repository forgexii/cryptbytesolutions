"""
Cryptbyte Solutions - Services Application Tests
"""

from django.test import TestCase
from django.urls import reverse


class ServicesViewTestCase(TestCase):
    """Verifies that the public services catalog renders successfully."""

    def test_services_page_status_code(self):
        """Ensure services page responds with HTTP 200 OK."""
        response = self.client.get(reverse('services:services'))
        self.assertEqual(response.status_code, 200)
