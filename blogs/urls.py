from django.urls import path

from .views import (
    blog_create_view,
    blog_detail_view,
    blog_list_view,
)

urlpatterns = [
    path("<int:pk>/", blog_detail_view, name="blog_detail"),
    path("new/", blog_create_view, name="blog_new"),
    path("", blog_list_view, name="blog_list"),
]
