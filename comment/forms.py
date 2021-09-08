from django import forms
from comment.models import Comment


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']