from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import CommentForm, BlogForm
from .models import Blog, Comment

# Create your views here.


@login_required
@ensure_csrf_cookie
def blog_list_view(request):
    blogs = Blog.objects.all().order_by("-date")
    paginator = Paginator(blogs, 5)  # Show 5 blogs per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "blog_list.html"
    return TemplateResponse(request, template, {"page_obj": page_obj})


@login_required
@ensure_csrf_cookie
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
    did_user_comment = blog.comments.filter(author=request.user).exists()
    form = CommentForm()
    context = {
        "blog": blog,
        "comments": comments,
        "form": form,
        "total_comments": total_comments,
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
