from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Blog, Comment, Like

# Create your views here.


@login_required
def blog_list_view(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)  # Show 5 blogs per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "blog_list.html"
    TemplateResponse(request, template, {"page_obj": page_obj})


@login_required
def blog_detail_view(request, id):
    blog = get_object_or_404(Blog.objects.all(), id=id)
    blog_instance = Blog.objects.get(id=id)
    comments = blog_instance.blog.all()
    form = CommentForm()
    context = {"blog": blog, "comments": comments, "form": form}
    template = "blog_detail.html"
    TemplateResponse(request, template, context)
