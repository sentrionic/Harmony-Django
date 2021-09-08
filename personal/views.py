from django.shortcuts import render, redirect
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from story.views import get_story_queryset, get_liked_story_queryset, get_followed_story_queryset
from story.utils import liked_post, unlike_post, like_post, get_time_ago
from story.models import StoryPost, StoryLikes
from comment.models import Comment

STORY_POSTS_PER_PAGE = 10


def home_screen_view(request, *args, **kwargs):
    context = {}

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    if request.POST:
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        if 'heart_button' in request.POST:
            context['liked'] = handle_like(user, request.POST.get('story', ''))

    story_posts = sorted(get_story_queryset(query), key=attrgetter('date_published'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    story_posts_paginator = Paginator(story_posts, STORY_POSTS_PER_PAGE)

    try:
        story_posts = story_posts_paginator.page(page)
    except PageNotAnInteger:
        story_posts = story_posts_paginator.page(STORY_POSTS_PER_PAGE)
    except EmptyPage:
        story_posts = story_posts_paginator.page(story_posts_paginator.num_pages)

    for post in story_posts:
        post.comments = Comment.objects.filter(post=post).count()
        post.likes = StoryLikes.objects.filter(post=post).count()
        post.liked = request.user.is_authenticated and liked_post(request.user, post)
        post.date = get_time_ago(post.date_published)

    context['story_posts'] = story_posts
    return render(request, "personal/home.html", context)


def liked_screen_view(request, *args, **kwargs):
    context = {}

    if not request.user.is_authenticated:
        return redirect("login")

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    if request.POST:
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        if 'heart_button' in request.POST:
            context['liked'] = handle_like(user, request.POST.get('story', ''))

    story_posts = sorted(get_liked_story_queryset(request.user, query), key=attrgetter('date_published'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    story_posts_paginator = Paginator(story_posts, STORY_POSTS_PER_PAGE)

    try:
        story_posts = story_posts_paginator.page(page)
    except PageNotAnInteger:
        story_posts = story_posts_paginator.page(STORY_POSTS_PER_PAGE)
    except EmptyPage:
        story_posts = story_posts_paginator.page(story_posts_paginator.num_pages)

    for post in story_posts:
        post.comments = Comment.objects.filter(post=post).count()
        post.likes = StoryLikes.objects.filter(post=post).count()
        post.liked = request.user.is_authenticated and liked_post(request.user, post)
        post.date = get_time_ago(post.date_published)

    context['story_posts'] = story_posts
    return render(request, "personal/home.html", context)


def followed_screen_view(request, *args, **kwargs):
    context = {}

    if not request.user.is_authenticated:
        return redirect("login")

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    if request.POST:
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        if 'heart_button' in request.POST:
            context['liked'] = handle_like(user, request.POST.get('story', ''))

    story_posts = sorted(get_followed_story_queryset(request.user, query), key=attrgetter('date_published'),
                         reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    story_posts_paginator = Paginator(story_posts, STORY_POSTS_PER_PAGE)

    try:
        story_posts = story_posts_paginator.page(page)
    except PageNotAnInteger:
        story_posts = story_posts_paginator.page(STORY_POSTS_PER_PAGE)
    except EmptyPage:
        story_posts = story_posts_paginator.page(story_posts_paginator.num_pages)

    for post in story_posts:
        post.comments = Comment.objects.filter(post=post).count()
        post.likes = StoryLikes.objects.filter(post=post).count()
        post.liked = request.user.is_authenticated and liked_post(request.user, post)
        post.date = get_time_ago(post.date_published)

    context['story_posts'] = story_posts
    return render(request, "personal/home.html", context)


def api_view(request):
    return render(request, "personal/api.html", {})


def handle_like(user, title):
    try:
        story_post = StoryPost.objects.get(title=title)
    except StoryPost.DoesNotExist:
        return False

    if liked_post(user, story_post):
        return unlike_post(user, story_post)
    else:
        return like_post(user, story_post)
