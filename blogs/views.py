from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Blog, Comment, Like

# Create your views here.


def blog_list_view(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)  # Show 5 blogs per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "blog_list.html"
    TemplateResponse(request, template, {"page_obj": page_obj})
