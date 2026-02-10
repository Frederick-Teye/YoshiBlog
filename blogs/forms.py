from django.forms import ModelForm, Textarea
from django import forms

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
    tags = forms.CharField(
        help_text="Enter tags separated by commas, e.g., python, django, web development",
        required=False,
    )

    class Meta:
        model = Blog
        fields = (
            "tags",
            "title",
            "body",
        )
