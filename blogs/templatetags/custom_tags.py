from django import template
from django.shortcuts import get_object_or_404
from blogs.models import Blog, Comment

register = template.Library()

@register.simple_tag(takes_context=True)
def user_likes_blog(context, pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    user = context["request"].user
    return blog.blog_likes.filter(id=user.id).exists()


@register.simple_tag(takes_context=True)
def user_likes_comment(context, pk):
    comment = get_object_or_404(Comment.objects.all(), pk=pk)
    user = context["request"].user
    return comment.comment_likes.filter(id=user.id).exists()


@register.simple_tag()
def total_blog_likes(pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    return blog.blog_likes.count()


@register.simple_tag()
def total_comment_likes(pk):
    comment = get_object_or_404(Comment.objects.all(), pk=pk)
    return comment.comment_likes.count()


@register.simple_tag()
def total_comments(pk):
    blog_instance = Blog.objects.get(pk=pk)
    return blog_instance.comments.count()
