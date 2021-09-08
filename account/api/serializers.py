from rest_framework import serializers

from account.models import Account, Follows
from story.models import StoryPost
from story.utils import does_user_follow_profile

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):

    followers = serializers.SerializerMethodField('get_followers_count')
    following = serializers.SerializerMethodField('get_following_count')
    posts = serializers.SerializerMethodField('get_post_count')

    class Meta:
        model = Account
        fields = ['pk', 'email', 'username', 'display_name', 'image', 'posts', 'followers', 'following', 'description',
                  'website']

    def get_post_count(self, account):
        return StoryPost.objects.filter(author=account).count()

    def get_followers_count(self, account):
        return Follows.objects.filter(following=account).count()

    def get_following_count(self, account):
        return Follows.objects.filter(follower=account).count()
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


class AccountProfileSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField('check_if_following')
    posts = serializers.SerializerMethodField('get_post_count')
    followers = serializers.SerializerMethodField('get_followers_count')
    following = serializers.SerializerMethodField('get_following_count')

    class Meta:
        model = Account
        fields = ['pk', 'username', 'display_name', 'image', 'posts', 'followers', 'following', 'description', 'website', 'follow']

    def check_if_following(self, account):
        return does_user_follow_profile(self.context['request'].user, account.username)

    def get_post_count(self, account):
        return StoryPost.objects.filter(author=account).count()

    def get_followers_count(self, account):
        return Follows.objects.filter(following=account).count()

    def get_following_count(self, account):
        return Follows.objects.filter(follower=account).count()


class ProfileFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follows
        fields = []