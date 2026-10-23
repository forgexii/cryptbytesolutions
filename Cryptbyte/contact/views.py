"""
Cryptbyte Solutions - Contact Application Views

Handles the contact form presentation, communication channels, and direct enquiry interfaces.
"""

from django.shortcuts import render


def contact(request):
    """
    Render the public Contact page.

    Provides direct communication channels (email, phone, office coordinates, socials)
    along with the primary project brief enquiry form.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered contact page template.
    """
    return render(request, 'contact/index.html')
