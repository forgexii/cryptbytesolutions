"""
Cryptbyte Solutions - Blogs Application Views

Provides public views for listing editorial insights with categories and keyword search,
as well as detailed single-article views with related post recommendations.
"""

from django.shortcuts import render, Http404
from django.db.models import Q
from .models import BlogPost, BlogCategory


def blog_list(request):
    """
    Render the public blog directory with category filtering and keyword search.

    Supports:
    - ?category=<slug>: Filters articles matching category slug or name.
    - ?q=<keyword>: Case-insensitive search across title, excerpt, content, author, and tags.

    Identifies a lead featured article for hero placement and lists remaining articles in grid.

    Args:
        request (HttpRequest): Standard Django HTTP request.

    Returns:
        HttpResponse: Rendered blog index template.
    """
    category_param = request.GET.get('category', '').strip().lower()
    search_query = request.GET.get('q', '').strip()

    # Query published articles with category relations preloaded
    posts_qs = BlogPost.objects.filter(is_published=True).select_related('category')

    # Apply keyword search across multiple content fields
    if search_query:
        posts_qs = posts_qs.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(category_name__icontains=search_query)
        )

    # Apply category filter if active
    if category_param and category_param != 'all':
        posts_qs = posts_qs.filter(
            Q(category__slug=category_param) | Q(category_name__iexact=category_param)
        )

    posts = list(posts_qs)
    categories = BlogCategory.objects.all()

    total_db_articles = BlogPost.objects.filter(is_published=True).count()
    total_categories_count = categories.count()

    # Determine featured hero post and remaining grid articles
    featured_post = None
    regular_posts = []

    if posts:
        # Prioritize explicit is_featured flag, else first post
        featured_candidates = [p for p in posts if p.is_featured]
        if featured_candidates:
            featured_post = featured_candidates[0]
            regular_posts = [p for p in posts if p.id != featured_post.id]
        else:
            featured_post = posts[0]
            regular_posts = posts[1:]

    return render(request, 'blogs/index.html', {
        'featured_post': featured_post,
        'posts': regular_posts,
        'all_posts_count': len(posts),
        'total_db_articles': total_db_articles,
        'total_categories_count': total_categories_count,
        'categories': categories,
        'current_category': category_param or 'all',
        'search_query': search_query,
    })


def blog_detail(request, slug):
    """
    Render a single full-length blog article.

    Allows staff users to preview unpublished draft articles while ensuring the public
    only accesses published posts. Fetches related articles based on category or tags.

    Args:
        request (HttpRequest): Standard Django HTTP request.
        slug (str): Unique URL slug identifier for the article.

    Returns:
        HttpResponse: Rendered article detail page.

    Raises:
        Http404: If article does not exist or is unpublished for non-staff visitors.
    """
    if request.user.is_staff:
        post = BlogPost.objects.filter(slug=slug).select_related('category').first()
    else:
        post = BlogPost.objects.filter(slug=slug, is_published=True).select_related('category').first()

    if not post:
        raise Http404("Article not found")

    # Query related reading suggestions
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id).filter(
        Q(category=post.category) | Q(tags__icontains=post.tags[:10] if post.tags else '')
    )[:3]

    return render(request, 'blogs/detail.html', {
        'post': post,
        'related_posts': related_posts,
    })
