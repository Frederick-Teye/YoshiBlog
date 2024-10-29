from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Blog, Comment, Like

# Create your views here.
