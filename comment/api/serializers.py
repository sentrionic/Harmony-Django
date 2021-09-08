from rest_framework import serializers
from django.conf import settings
from comment.models import Comment


class StoryCommentsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Comment
        fields = ['pk', 'comment', 'image', 'date_published', 'likes', 'username']

    def get_username_from_author(self, story_post):
        username = story_post.author.username
        return username

    def validate_image_url(self, story_post):
        image = story_post.author.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url


class StoryPostCreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'author', 'comment']

    def save(self):
        try:
            comment = Comment(
                author=self.validated_data['author'],
                comment=self.validated_data['comment'],
                post=self.validated_data['post'],
            )

            comment.save()
            return comment
        except KeyError:
            raise serializers.ValidationError({"response": "Error posting the comment."})