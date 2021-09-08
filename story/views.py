from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from story.models import StoryPost, StoryLikes
from comment.models import Comment
from story.forms import CreateStoryPostForm, UpdateStoryPostForm, get_tags, DeleteStoryPostForm, LikeStoryPostForm
from account.models import Account, Follows
from story.utils import liked_post, unlike_post, like_post, get_time_ago
from comment.forms import CommentPostForm


def create_story_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateStoryPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        author.save()
        obj.author = author
        obj.tags = get_tags(request.POST.get('caption'))
        obj.save()
        form = CreateStoryPostForm()
        return redirect('home')

    context['form'] = form

    return render(request, 'story/create_story.html', context)


def detail_story_view(request, slug):
    context = {}
    story_post = get_object_or_404(StoryPost, slug=slug)

    if request.POST:
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        if 'heart_button' in request.POST:
            if liked_post(user, story_post):
                context['liked'] = unlike_post(user, story_post)
            else:
                context['liked'] = like_post(user, story_post)

        elif 'comment_posted' in request.POST:
            form = CommentPostForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                author = Account.objects.filter(email=user.email).first()
                story_post.save()
                obj.author = author
                obj.post = story_post
                obj.save()

    query = Comment.objects.filter(post=story_post)
    story_post.comments = query.count()
    story_post.likes = StoryLikes.objects.filter(post=story_post).count()
    context['date'] = get_time_ago(story_post.date_published)
    context['story_post'] = story_post
    context['liked'] = request.user.is_authenticated and liked_post(request.user, story_post)
    context['comments'] = query

    return render(request, 'story/detail_story.html', context)


def delete_story_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    story_post = get_object_or_404(StoryPost, slug=slug)

    if story_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = DeleteStoryPostForm(request.POST, instance=story_post)
        if form.is_valid():
            story_post.delete()
            context['success_message'] = "Deleted"
            user.save()
            return redirect('home')

    context['story_post'] = story_post

    return render(request, 'story/delete_story.html', context)


def edit_story_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    story_post = get_object_or_404(StoryPost, slug=slug)

    if story_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = UpdateStoryPostForm(request.POST or None, request.FILES or None, instance=story_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            story_post = obj

    form = UpdateStoryPostForm(
        initial={
            "caption": story_post.caption,
            "image": story_post.image,
        }
    )
    context['form'] = form

    return render(request, 'story/edit_story.html', context)


def get_story_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = StoryPost.objects.filter(
            Q(tags__contains=q) |
            Q(caption__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))


def get_liked_story_queryset(user, query):
    queryset = []

    likes = StoryLikes.objects.filter(
        Q(author=user)
    ).select_related()

    for like in likes:
        post = StoryPost.objects.get(
            Q(pk=like.post_id)
        )
        queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))


def get_followed_story_queryset(user, query):
    queryset = []

    followed = Follows.objects.filter(
        Q(follower_id=user)
    ).select_related()

    for follow in followed:
        posts = StoryPost.objects.filter(
            Q(author=follow.following_id)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))

