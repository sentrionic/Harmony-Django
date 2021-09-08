from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication

from story.models import StoryPost, StoryLikes
from comment.models import Comment
from story.api.serializers import StoryPostSerializer, StoryPostUpdateSerializer, StoryPostCreateSerializer, \
    StoryPostLikeSerializer
from comment.api.serializers import StoryCommentsSerializer, StoryPostCreateCommentSerializer
from story.utils import unlike_post, like_post, liked_post
from account.models import Follows, Account

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

PAGINATION_NUM_PAGES = 10


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_story_view(request, slug):
    try:
        story_post = StoryPost.objects.get(slug=slug)
    except StoryPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StoryPostSerializer(story_post, context={'request': request})
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_story_view(request, slug):
    try:
        story_post = StoryPost.objects.get(slug=slug)
    except StoryPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if story_post.author != user:
        return Response({'response': "You don't have permission to edit that."})

    if request.method == 'PUT':
        serializer = StoryPostUpdateSerializer(story_post, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = UPDATE_SUCCESS
            data['pk'] = story_post.pk
            data['caption'] = story_post.caption
            data['tags'] = story_post.tags
            data['slug'] = story_post.slug
            data['date_updated'] = story_post.date_updated
            image_url = str(request.build_absolute_uri(story_post.image.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['image'] = image_url
            data['username'] = story_post.author.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_story_view(request, slug):
    try:
        story_post = StoryPost.objects.get(slug=slug)
    except StoryPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if story_post.author != user:
        return Response({'response': "You don't have permission to delete that."})

    if request.method == 'DELETE':
        operation = story_post.delete()
        data = {}
        if operation:
            data['response'] = DELETE_SUCCESS
        return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_story_view(request):
    if request.method == 'POST':

        data = request.data
        data['author'] = request.user.pk
        serializer = StoryPostCreateSerializer(data=data)

        data = {}
        if serializer.is_valid():
            story_post = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['pk'] = story_post.pk
            data['caption'] = story_post.caption
            data['tags'] = story_post.tags
            data['slug'] = story_post.slug
            data['date_updated'] = story_post.date_updated
            image_url = str(request.build_absolute_uri(story_post.image.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            data['image'] = image_url
            data['username'] = story_post.author.username
            data['profile_image'] = story_post.author.image.url
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_comment_view(request, slug):
    if request.method == 'POST':

        data = request.data.copy()
        data['author'] = request.user.pk

        try:
            story_post = StoryPost.objects.get(slug=slug)
        except StoryPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data['post'] = story_post.pk
        serializer = StoryPostCreateCommentSerializer(data=data)

        data = {}
        if serializer.is_valid():
            comment = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['pk'] = comment.pk
            data['comment'] = comment.comment
            data['date_published'] = comment.date_published
            data['username'] = comment.author.username
            data['post'] = story_post.slug
            data['image'] = comment.author.image.url
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_like_story_view(request, slug):
    if request.method == 'POST':
        data = request.data
        serializer = StoryPostLikeSerializer(data=data)
        user = request.user
        try:
            story_post = StoryPost.objects.get(slug=slug)
        except StoryPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            data = {}
            if not liked_post(user, story_post):
                like_post(user, story_post)
                data['response'] = 'Liked Post'
            else:
                unlike_post(user, story_post)
                data['response'] = 'Unliked Post'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_is_author_of_storypost(request, slug):
    try:
        story_post = StoryPost.objects.get(slug=slug)
    except StoryPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    user = request.user
    if story_post.author != user:
        data['response'] = "You don't have permission to edit that."
        return Response(data=data)
    data['response'] = "You have permission to edit that."
    return Response(data=data)


class ApiBlogListView(ListAPIView):
    queryset = StoryPost.objects.all()
    serializer_class = StoryPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('caption', 'tags', 'author__username', 'author__display_name')


class ApiFollowedListView(ListAPIView):
    serializer_class = StoryPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = []
        followed = Follows.objects.filter(
            follower_id=self.request.user
        ).select_related()

        for follow in followed:
            posts = StoryPost.objects.filter(
                author=follow.following_id
            ).distinct()
            for post in posts:
                queryset.append(post)

        story_posts = StoryPost.objects.filter(
            author=self.request.user.id
        ).distinct()

        for story in story_posts:
            queryset.append(story)

        return queryset

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('caption', 'tags', 'author__username', 'author__display_name')


class ApiLikedListView(ListAPIView):
    serializer_class = StoryPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = []
        likes = StoryLikes.objects.filter(
            author=self.request.user
        ).select_related()

        for like in likes:
            post = StoryPost.objects.get(
                pk=like.post_id
            )
            queryset.append(post)

        return queryset

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('caption', 'tags', 'author__username', 'author__display_name')


class ApiProfileStoryListView(ListAPIView):
    serializer_class = StoryPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        try:
            account = Account.objects.get(username__iexact=self.request.GET.get('username'))
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return StoryPost.objects.filter(author=account)

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('caption', 'tags', 'author__username', 'author__display_name')


class ApiStoryCommentListView(ListAPIView):
    serializer_class = StoryCommentsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        try:
            story_post = StoryPost.objects.get(slug=self.request.GET.get('slug'))
        except StoryPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Comment.objects.filter(post=story_post)

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('post__slug')