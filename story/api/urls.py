from django.urls import path

from story.api.views import (
    api_detail_story_view,
    api_update_story_view,
    api_delete_story_view,
    api_create_story_view,
    api_is_author_of_storypost,
    api_like_story_view,
    api_create_comment_view,
    ApiBlogListView,
    ApiFollowedListView,
    ApiLikedListView,
    ApiProfileStoryListView,
    ApiStoryCommentListView,
)

app_name = 'story'

urlpatterns = [
    path('<slug>/', api_detail_story_view, name="detail"),
    path('<slug>/update', api_update_story_view, name="update"),
    path('<slug>/delete', api_delete_story_view, name="delete"),
    path('<slug>/comment', api_create_comment_view, name="comment"),
    path('create', api_create_story_view, name="create"),
    path('list', ApiBlogListView.as_view(), name="list"),
    path('<slug>/is_author', api_is_author_of_storypost, name="is_author"),
    path('comments', ApiStoryCommentListView.as_view(), name="comments"),
    path('<slug>/like', api_like_story_view, name='like'),
    path('followed', ApiFollowedListView.as_view(), name="followed"),
    path('liked', ApiLikedListView.as_view(), name="liked"),
    path('stories', ApiProfileStoryListView.as_view(), name="profile_story_list")
]
