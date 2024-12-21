from django.forms import ModelForm, Textarea

from .models import Comment, Blog


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            "title",
            "body",
        )
