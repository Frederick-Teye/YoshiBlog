from django.forms import ModelForm, Textarea

from .models import Comment, Blog


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
        widgets = {
            "comment": Textarea(
                attrs={
                    "cols": 80,
                    "rows": 1,
                    "class": "no-scrollbars",
                }
            ),
        }


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = (
            "title",
            "body",
        )
