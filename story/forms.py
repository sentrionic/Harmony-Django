from django import forms

from story.models import StoryPost, StoryLikes
from story.utils import get_tags

class CreateStoryPostForm(forms.ModelForm):
    class Meta:
        model = StoryPost
        fields = ['caption', 'image']


class UpdateStoryPostForm(forms.ModelForm):
    class Meta:
        model = StoryPost
        fields = ['caption', 'image']

    def save(self, commit=True):
        story_post = self.instance
        story_post.caption = self.cleaned_data['caption']
        story_post.tags = get_tags(self.cleaned_data['caption'])

        if self.cleaned_data['image']:
            story_post.image = self.cleaned_data['image']

        if commit:
            story_post.save()
        return story_post


class DeleteStoryPostForm(forms.ModelForm):
    class Meta:
        model = StoryPost
        fields = []


class LikeStoryPostForm(forms.ModelForm):
    class Meta:
        model = StoryLikes
        fields = ['post']