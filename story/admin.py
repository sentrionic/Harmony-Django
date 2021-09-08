from django.contrib import admin

from story.models import StoryPost, StoryLikes

admin.site.register(StoryPost)
admin.site.register(StoryLikes)
