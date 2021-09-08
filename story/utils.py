from story.models import StoryPost, StoryLikes
from account.models import Account, Follows

import datetime
import cv2
import os
from math import floor


def is_image_aspect_ratio_valid(img_url):
    img = cv2.imread(img_url)
    dimensions = tuple(img.shape[1::-1])  # gives: (width, height)
    # print("dimensions: " + str(dimensions))
    aspect_ratio = dimensions[0] / dimensions[1]  # divide w / h
    # print("aspect_ratio: " + str(aspect_ratio))
    if aspect_ratio < 1:
        return False
    return True


def is_image_size_valid(img_url, mb_limit):
    image_size = os.path.getsize(img_url)
    # print("image size: " + str(image_size))
    if image_size > mb_limit:
        return False
    return True


def liked_post(user, story_post):
    return StoryLikes.objects.filter(author=Account.objects.filter(email=user.email).first(),
                                     post=StoryPost.objects.filter(pk=story_post.pk).first()).exists()


def unlike_post(user, story_post):
    like = StoryLikes.objects.get(author=Account.objects.filter(email=user.email).first(),
                                  post=StoryPost.objects.filter(pk=story_post.pk).first())
    like.delete()
    return False


def like_post(user, story_post):
    like = StoryLikes(author=Account.objects.filter(email=user.email).first(),
                      post=StoryPost.objects.filter(pk=story_post.pk).first())
    like.save()
    return True


def does_user_follow_profile(user, profile_username):
    return Follows.objects.filter(follower_id=Account.objects.get(email=user.email),
                                  following_id=Account.objects.get(username__iexact=profile_username)).exists()


def unfollow_profile(user, profile):
    follows = Follows.objects.get(follower_id=Account.objects.get(email=user.email),
                                  following_id=Account.objects.get(username__iexact=profile.username))
    follows.delete()
    return False


def follow_profile(user, profile):
    follows = Follows(follower_id=Account.objects.get(email=user.email).pk,
                   following_id=Account.objects.get(username__iexact=profile.username).pk)
    follows.save()
    return True

def get_time_ago(story_date):

    SECOND_MILLIS = 1000
    MINUTE_MILLIS = 60 * SECOND_MILLIS
    HOUR_MILLIS = 60 * MINUTE_MILLIS
    DAY_MILLIS = 24 * HOUR_MILLIS

    time = story_date.timestamp() * 1000
    now = datetime.datetime.now().timestamp() * 1000

    if time > now or time <= 0:
        return story_date

    diff = now - time

    if diff < MINUTE_MILLIS:
        return "just now"

    elif diff < 2 * MINUTE_MILLIS:
        return "a minute ago"
    elif diff < 50 * MINUTE_MILLIS:
        return str(floor(diff / MINUTE_MILLIS)) + " minutes ago"
    elif diff < 90 * MINUTE_MILLIS:
        return "an hour ago"
    elif diff < 24 * HOUR_MILLIS:
        return str(floor(diff / HOUR_MILLIS)) + "h ago"
    elif diff < 48 * HOUR_MILLIS:
        return "yesterday"
    elif diff < 30 * DAY_MILLIS:
        return str(floor(diff / DAY_MILLIS)) + " days ago"
    else:
        return story_date


def get_tags(caption):
    if "#" in caption:
        out_str = ""
        found_word = False

        for c in caption:
            if c == '#':
                found_word = True
                out_str += c
            else:
                if found_word:
                    out_str += c

            if c == ' ':
                found_word = False

        out_str = out_str.replace(" ", "").replace("#", ",#")
        return out_str[1:]

    return ""
