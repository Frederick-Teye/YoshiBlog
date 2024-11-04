from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from .forms import CommentForm, BlogForm
from .models import Blog, Comment, BlogLike

# Create your views here.


@login_required
def blog_list_view(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)  # Show 5 blogs per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "blog_list.html"
    return TemplateResponse(request, template, {"page_obj": page_obj})


@login_required
def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog.objects.all(), pk=pk)
    blog_instance = Blog.objects.get(pk=pk)
    comments = blog_instance.comments.all()
    form = CommentForm()
    context = {"blog": blog, "comments": comments, "form": form}
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
    blog.delete
    return redirect('blog_list')