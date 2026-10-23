"""
Cryptbyte Solutions - Services Application Views

Presents high-level technical services, system design consulting, and delivery capabilities.
"""

from django.shortcuts import render


def services(request):
    """
    Render the public Services catalog page.

    Displays enterprise software engineering, AI/ML integration, cybersecurity,
    and cloud infrastructure service offerings.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered services catalog template.
    """
    return render(request, 'services/index.html')
