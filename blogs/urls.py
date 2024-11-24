from django.urls import path

from .views import (
    blog_create_view,
    blog_delete_view,
    blog_detail_view,
    blog_list_view,
    blog_update_view,
    blog_like_view,
)

urlpatterns = [
    path("<int:pk>/", blog_detail_view, name="blog_detail"),
    path("<int:pk>/delete/", blog_delete_view, name="blog_delete"),
    path("<int:pk>/edit/", blog_update_view, name="blog_edit"),
    path("<int:ip>/like/", blog_like_view, name="blog_like"),
    path("new/", blog_create_view, name="blog_new"),
    path("", blog_list_view, name="blog_list"),
]
