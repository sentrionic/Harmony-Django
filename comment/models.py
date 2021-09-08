from django.db import models
from django.conf import settings
from story.models import StoryPost


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(StoryPost, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200, null=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    likes = models.IntegerField(verbose_name="likes", default=0)