from django.shortcuts import render, get_object_or_404, Http404
from django.db.models import Q
from .models import BlogPost, BlogCategory


def blog_list(request):
    """List of all blog articles with category filtering and search."""
    category_param = request.GET.get('category', '').strip().lower()
    search_query = request.GET.get('q', '').strip()

    posts_qs = BlogPost.objects.filter(is_published=True).select_related('category')

    # Apply search filter
    if search_query:
        posts_qs = posts_qs.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(category_name__icontains=search_query)
        )

    # Apply category filter
    if category_param and category_param != 'all':
        posts_qs = posts_qs.filter(
            Q(category__slug=category_param) | Q(category_name__iexact=category_param)
        )

    posts = list(posts_qs)
    categories = BlogCategory.objects.all()

    total_db_articles = BlogPost.objects.filter(is_published=True).count()
    total_categories_count = categories.count()

    # Determine featured post and remaining posts
    featured_post = None
    regular_posts = []

    if posts:
        # Prefer post marked is_featured=True, else first post
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
    """Detailed view for a single blog post."""
    if request.user.is_staff:
        post = BlogPost.objects.filter(slug=slug).select_related('category').first()
    else:
        post = BlogPost.objects.filter(slug=slug, is_published=True).select_related('category').first()

    if not post:
        raise Http404("Article not found")

    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id).filter(
        Q(category=post.category) | Q(tags__icontains=post.tags[:10] if post.tags else '')
    )[:3]

    return render(request, 'blogs/detail.html', {
        'post': post,
        'related_posts': related_posts,
    })
