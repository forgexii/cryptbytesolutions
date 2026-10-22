from django.shortcuts import render


def services(request):
    """Public Services page for Cryptbyte Solutions."""
    return render(request, 'services/index.html')
