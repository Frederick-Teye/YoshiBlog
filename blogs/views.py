from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import CommentForm, BlogForm
from .models import Blog, Comment

# Create your views here.


@login_required
def blog_list_view(request):
    blogs = Blog.objects.all().order_by("-date")
    paginator = Paginator(blogs, 3)  # Show 3 blogs per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "blog_list.html"
    return TemplateResponse(request, template, {"page_obj": page_obj})


@login_required
def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    # blog_instance = Blog.objects.get(pk=pk)
    sort_comments_by = request.COOKIES.get("sort_comment_by", "newest")
    if sort_comments_by == "top":
        comments = blog.comments.all().order_by("-likes")
        is_ordered_by_likes = True
    else:
        comments = blog.comments.all().order_by("-created_at")
        is_ordered_by_likes = False
    total_comments = blog.comments.count()
    total_likes = blog.likes.count()
    did_user_comment = blog.comments.filter(author=request.user).exists()
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
    template = "blog_detail.html"
    return TemplateResponse(request, template, context)


@login_required
def blog_create_view(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            blog_model_instance = form.save()
            return redirect("blog_detail", pk=blog_model_instance.pk)
    else:
        form = BlogForm()

    return TemplateResponse(request, "blog_new.html", {"form": form})


@login_required
def blog_update_view(request, pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.instance.author = request.user
            blog_model_instance = form.save()
            return redirect("blog_detail", pk=blog_model_instance.pk)
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
    if request.path_info == "/blogs/" + str(pk) + "/like/":
        blog = get_object_or_404(Blog.objects.all(), id=request.POST.get("blog_id"))
        is_liked = False
        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)
            is_liked = False
        else:
            blog.likes.add(request.user)
            is_liked = True
        context = {
            "blog": blog,
            "is_liked": is_liked,
            "total_likes": blog.likes.count(),
        }
        template = "blog_detail_components/reaction_section.html"
    else:
        blog = get_object_or_404(Blog.objects.all(), id=request.POST.get("blog_id"))
        is_liked = False
        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)
            is_liked = False
        else:
            blog.likes.add(request.user)
            is_liked = True
        context = {
            "blog": blog,
            "is_liked": is_liked,
            "total_likes": blog.likes.count(),
        }
        template = "blog_list_components/reaction_section.html"
    return TemplateResponse(request, template, context)


@login_required
def comment_delete_view(request, pk, comment_pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    comment = get_object_or_404(Comment.objects.all(), blog=blog, pk=comment_pk)
    comment.delete()
    return redirect("blog_detail", pk=pk)


@login_required
def comment_update_view(request, pk, comment_pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    comment = get_object_or_404(Comment.objects.all(), blog=blog, pk=comment_pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect("blog_detail", pk=blog.pk)
    else:
        form = CommentForm(instance=comment)

    return TemplateResponse(
        request, "blog_detail_components/comment_edit_form.html", {"form": form}
    )


@login_required
def comment_create_view(
    request, pk
):  # pk is the pk of the blog which comment belong to
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        form.instance.author = request.user
        form.instance.blog = blog
        comment_model_instance = form.save()
        return TemplateResponse(
            request,
            "blog_detail_components/comment.html",
            {"comment": comment_model_instance},
        )


@login_required
def comment_like_view(request, pk, comment_pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    comment = get_object_or_404(Comment.objects.all(), blog=blog, pk=comment_pk)
    if (
        request.user in comment.likes.all()
    ):  # new style I learnt to filter which easy to understand by just looking
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return render(
        request,
        "blog_detail_components/comment_reaction_section.html",
        {"comment": comment},
    )
