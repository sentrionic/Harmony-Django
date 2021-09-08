from django.urls import path
from story.views import (
    create_story_view,
    detail_story_view,
    edit_story_view,
    delete_story_view,
)

app_name = 'story'

urlpatterns = [
    path('create/', create_story_view, name="create"),
    path('<slug>/', detail_story_view, name="detail"),
    path('<slug>/edit/', edit_story_view, name="edit"),
    path('<slug>/delete/', delete_story_view, name="delete"),
]
