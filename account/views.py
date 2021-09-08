from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from story.models import StoryPost
from account.models import Account, Follows
from story.utils import does_user_follow_profile, unfollow_profile, follow_profile

STORY_POSTS_PER_PAGE = 10


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "account/login.html", context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
                "display_name": request.POST['display_name'],
                "website": request.POST['website'],
                "description": request.POST['description']
            }

            form.save()
            form.initial['image'] = request.user.image
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(

            initial={
                "email": request.user.email,
                "username": request.user.username,
                "display_name": request.user.display_name,
                "description": request.user.description,
                "website": request.user.website,
                "image": request.user.image,
            }
        )

    context['account_form'] = form
    return render(request, "account/account.html", context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})


def view_personal_stories(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    story_posts = StoryPost.objects.filter(author=request.user)
    context['story_posts'] = story_posts
    return render(request, 'account/personal_stories.html', context)


def profile_view(request, username):
    context = {}
    profile = get_object_or_404(Account, username__iexact=username)

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    story_posts = sorted(get_profile_posts_query(profile, query), key=attrgetter('date_published'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    story_posts_paginator = Paginator(story_posts, STORY_POSTS_PER_PAGE)

    try:
        story_posts = story_posts_paginator.page(page)
    except PageNotAnInteger:
        story_posts = story_posts_paginator.page(STORY_POSTS_PER_PAGE)
    except EmptyPage:
        story_posts = story_posts_paginator.page(story_posts_paginator.num_pages)

    if request.POST:
        user = request.user
        if not user.is_authenticated:
            return redirect('must_authenticate')

        if does_user_follow_profile(user, profile.username):
            context['follows'] = unfollow_profile(user, profile)
        else:
            context['follows'] = follow_profile(user, profile)

    profile.posts = StoryPost.objects.filter(author=profile).count()
    profile.followers = Follows.objects.filter(following=profile).count()
    profile.following = Follows.objects.filter(follower=profile).count()
    context['profile'] = profile
    context['follows'] = request.user.is_authenticated and does_user_follow_profile(request.user, profile.username)
    context['stories'] = story_posts
    setattr(profile, 'email', "")
    return render(request, 'account/profile.html', context)


def get_profile_posts_query(profile, query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = StoryPost.objects.filter(
            author=profile
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))