from django import template
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import stringfilter
from blogs.models import Blog, Comment
import markdown as md

register = template.Library()


@register.simple_tag(takes_context=True)
def user_likes_blog(context, pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    user = context["request"].user
    return blog.likes.filter(id=user.id).exists()


@register.simple_tag(takes_context=True)
def user_likes_comment(context, pk):
    comment = get_object_or_404(Comment.objects.all(), pk=pk)
    user = context["request"].user
    return comment.likes.filter(id=user.id).exists()


@register.simple_tag()
def total_blog_likes(pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    return blog.likes.count()


@register.simple_tag()
def total_comment_likes(pk):
    comment = get_object_or_404(Comment.objects.all(), pk=pk)
    return comment.likes.count()


@register.simple_tag()
def total_comments(pk):
    blog_instance = Blog.objects.get(pk=pk)
    return blog_instance.comments.count()


@register.simple_tag()
def total_backticks(value: str):
    return value.count("```")


@register.simple_tag()
def close_code(value: str):
    if not isinstance(value, str):
        return value
    new_value = value + "\n```"
    return new_value


@register.filter
def truncatewords(blog_content: str, number_of_words: int):
    limit = limit_of_60_words(blog_content, number_of_words)
    new_string = blog_content[: limit + 1]
    new_string = new_string
    return new_string


def limit_of_words(blog_content: str, words_limit: int):
    word_counter = 0
    character_counter = 0
    in_word = False
    for i in blog_content:
        character_counter += 1
        if i != " ":
            if not in_word:
                word_counter += 1
                in_word = True
        else:
            in_word = False

        if word_counter == words_limit:
            break
    return character_counter


# markdown
@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=["markdown.extensions.fenced_code"])
