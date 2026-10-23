"""
Cryptbyte Solutions - Contact Application Tests
"""

from django.test import TestCase
from django.urls import reverse


class ContactViewTestCase(TestCase):
    """Verifies that the public contact page renders successfully."""

    def test_contact_page_status_code(self):
        """Ensure contact page responds with HTTP 200 OK."""
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)
