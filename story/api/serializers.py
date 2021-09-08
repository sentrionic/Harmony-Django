from rest_framework import serializers
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from story.models import StoryPost, StoryLikes
from story.utils import is_image_aspect_ratio_valid, is_image_size_valid, liked_post, get_tags
from comment.models import Comment

import os

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 10  # 10MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


class StoryPostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    profile_image = serializers.SerializerMethodField('get_profile_image_from_author')
    image = serializers.SerializerMethodField('validate_image_url')
    liked = serializers.SerializerMethodField('check_like_status')
    likes = serializers.SerializerMethodField('get_like_count')
    comments = serializers.SerializerMethodField('get_comment_count')

    class Meta:
        model = StoryPost
        fields = ['pk', 'slug', 'caption', 'image', 'date_published', 'likes', 'tags', 'username', 'liked', 'profile_image', 'comments']

    def get_username_from_author(self, story_post):
        username = story_post.author.username
        return username

    def validate_image_url(self, story_post):
        image = story_post.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url

    def check_like_status(self, story_post):
        return liked_post(self.context['request'].user, story_post)

    def get_like_count(self, story_post):
        return StoryLikes.objects.filter(post=story_post).count()

    def get_comment_count(self, story_post):
        return Comment.objects.filter(post=story_post).count()
        
    def get_profile_image_from_author(self, story_post):
        return story_post.author.image.url


class StoryPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryPost
        fields = ['caption', 'tags', 'image']

    def validate(self, story_post):
        try:
            image = story_post['image']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "That image is too large. Images must be less than 10 MB. Try a different image."})

            if not is_image_aspect_ratio_valid(url):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
        except KeyError:
            pass
        return story_post


class StoryPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryPost
        fields = ['caption', 'image', 'date_updated', 'author']

    def save(self):

        try:
            image = self.validated_data['image']

            story_post = StoryPost(
                author=self.validated_data['author'],
                caption=self.validated_data['caption'],
                tags=get_tags(self.validated_data['caption']),
                image=image,
            )

            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            # Check image size
            if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "That image is too large. Images must be less than 10 MB. Try a different image."})

            # Check image aspect ratio
            if not is_image_aspect_ratio_valid(url):
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
            story_post.save()
            return story_post
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a caption, some tags, and an image."})


class StoryPostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryLikes
        fields = []