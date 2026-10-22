from django.shortcuts import render


def contact(request):
    """Public Contact page for Cryptbyte Solutions."""
    return render(request, 'contact/index.html')
