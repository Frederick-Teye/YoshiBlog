from django.conf import settings
from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="comments"
    )  # added related_name argument
    comment = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment


class CommentLike(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = (
            "user",
            "comment",
        )  # Ensure a user can like a comment only once


class BlogLike(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = (
            "user",
            "blog",
        )  # Ensure a user can like a blog only once
