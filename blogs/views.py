import logging
import nh3
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.text import slugify
from .forms import CommentForm, BlogForm
from .models import Blog, Comment

logger = logging.getLogger(__name__)


def blog_list_view(request):
    blogs = Blog.objects.all().order_by("-date")
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    tag_names = list(Blog.objects.values_list("tags__name", flat=True).distinct())
    template = "blog_list.html"
    return TemplateResponse(
        request, template, {"page_obj": page_obj, "tags": tag_names}
    )


def blog_detail_view(request, pk, blog_slug):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    check_and_log_wrong_slug(request, blog, blog_slug)
    sort_comments_by = request.COOKIES.get("sort_comment_by", "newest")
    if sort_comments_by == "top":
        comments = blog.comments.all().order_by("-likes")
        is_ordered_by_likes = True
    else:
        comments = blog.comments.all().order_by("-created_at")
        is_ordered_by_likes = False
    total_comments = blog.comments.count()
    total_likes = blog.likes.count()
    if request.user.is_authenticated:
        did_user_comment = blog.comments.filter(author=request.user).exists()
    else:
        did_user_comment = False
    form = CommentForm()
    context = {
        "blog": blog,
        "comments": comments,
        "form": form,
        "total_comments": total_comments,
        "total_comments_minus_1": total_comments - 1,
        "total_likes": total_likes,
        "did_user_comment": did_user_comment,
        "is_ordered_by_likes": is_ordered_by_likes,
    }
    return TemplateResponse(request, "blog_detail.html", context)


@login_required
def blog_create_view(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            sanitized_title = sanitize_input(form.instance.title)
            sanitized_body = sanitize_input(form.instance.body)
            form.instance.title = sanitized_title
            form.instance.body = sanitized_body
            form.instance.author = request.user
            original_slug = slugify(sanitized_title)
            counter = 0
            while Blog.objects.filter(slug=original_slug).exists():
                counter += 1
                if counter == 1:
                    original_slug = original_slug + "-" + str(counter)
                elif 1 < counter <= 10:
                    original_slug = original_slug[:-1] + str(counter)
                elif counter > 10:
                    original_slug = original_slug[:-2] + str(counter)

            form.instance.slug = original_slug
            blog_model_instance = form.save()
            return redirect(
                "blog_detail",
                pk=blog_model_instance.pk,
                blog_slug=blog_model_instance.slug,
            )
    else:
        form = BlogForm()
    return TemplateResponse(request, "blog_new.html", {"form": form})


@login_required
def blog_update_view(request, pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            sanitize_title = sanitize_input(form.instance.title)
            sanitize_body = sanitize_input(form.instance.body)
            form.instance.title = sanitize_title
            form.instance.body = sanitize_body
            form.instance.author = request.user
            form.instance.slug = blog.slug
            blog_model_instance = form.save()
            return redirect(
                "blog_detail",
                pk=blog_model_instance.pk,
                blog_slug=blog_model_instance.slug,
            )
    else:
        form = BlogForm(instance=blog)
    return TemplateResponse(request, "blog_edit.html", {"form": form})


@login_required
def blog_delete_view(request, pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    blog.delete()
    return redirect("blog_list")


@login_required
def blog_like_view(request, pk):
    blog = get_object_or_404(Blog.objects.all(), id=request.POST.get("blog_id"))
    is_liked = False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
        is_liked = True

    total_comments = blog.comments.count()
    total_likes = blog.likes.count()
    if request.user.is_authenticated:
        did_user_comment = blog.comments.filter(author=request.user).exists()
    else:
        did_user_comment = False

    context = {
        "blog": blog,
        "is_liked": is_liked,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_comments_minus_1": total_comments - 1,
        "did_user_comment": did_user_comment,
    }

    if request.path_info == "/blogs/" + str(pk) + "/like/":
        template = "blog_detail_components/reaction_section.html"
    else:
        template = "blog_list_components/reaction_section.html"
    return TemplateResponse(request, template, context)


@login_required
def comment_delete_view(request, pk, blog_slug, comment_pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    comment = get_object_or_404(Comment.objects.all(), blog=blog, pk=comment_pk)
    comment.delete()
    return redirect("blog_detail", pk=pk, blog_slug=blog_slug)


@login_required
def comment_update_view(request, pk, blog_slug, comment_pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    comment = get_object_or_404(Comment.objects.all(), blog=blog, pk=comment_pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            sanitize_comment = sanitize_input(form.instance.comment)
            form.instance.comment = sanitize_comment
            form.instance.author = request.user
            form.save()
            return redirect("blog_detail", pk=blog.pk, blog_slug=blog_slug)
    else:
        form = CommentForm(instance=comment)
    return TemplateResponse(
        request, "blog_detail_components/comment_edit_form.html", {"form": form}
    )


@login_required
def comment_create_view(request, pk, blog_slug):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        sanitize_comment = sanitize_input(form.instance.comment)
        form.instance.comment = sanitize_comment
        form.instance.author = request.user
        form.instance.blog = blog
        comment_model_instance = form.save()
        return TemplateResponse(
            request,
            "blog_detail_components/comment.html",
            {"comment": comment_model_instance, "blog": blog},
        )


@login_required
def comment_like_view(request, pk, blog_slug, comment_pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    comment = get_object_or_404(Comment.objects.all(), blog=blog, pk=comment_pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return TemplateResponse(
        request,
        "blog_detail_components/comment_reaction_section.html",
        {"comment": comment, "blog": blog},
    )


def check_and_log_wrong_slug(request, blog, blog_slug):
    if blog_slug != blog.slug:
        referrer = request.META.get("HTTP_REFERRER", "No referrer")
        logger.error(
            "A bad slug was encountered: '%s'. Expected: '%s'. Referrer: %s",
            blog_slug,
            blog.slug,
            referrer,
        )


@login_required
def list_blog_tagged(request, tag_name):
    blogs = Blog.objects.filter(tags__name__in=[tag_name]).order_by("-date")
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    tag_names = list(Blog.objects.values_list("tags__name", flat=True).distinct())
    return TemplateResponse(
        request, "blog_list.html", {"page_obj": page_obj, "tags": tag_names}
    )


def sanitize_input(user_input):
    tags = nh3.ALLOWED_TAGS - {"article"}
    return nh3.clean(user_input, tags=tags)
