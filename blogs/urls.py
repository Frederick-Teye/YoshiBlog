from django.urls import path, include

from .views import (
    blog_create_view,
    blog_delete_view,
    blog_detail_view,
    blog_list_view,
    blog_update_view,
    blog_like_view,
    comment_create_view,
    comment_delete_view,
    comment_like_view,
    comment_update_view,
    list_blog_tagged,
)


comment_patterns = [
    path("<int:comment_pk>/delete/", comment_delete_view, name="comment_delete"),
    path("<int:comment_pk>/edit/", comment_update_view, name="comment_edit"),
    path("<int:comment_pk>/comment_like/", comment_like_view, name="comment_like"),
    path("new_comment/", comment_create_view, name="comment_new"),
]


urlpatterns = [
    path("<int:pk>/delete/", blog_delete_view, name="blog_delete"),
    path("<int:pk>/edit/", blog_update_view, name="blog_edit"),
    path("<int:pk>/like/", blog_like_view, name="blog_like"),
    path("<int:pk>/list_like/", blog_like_view, name="list_blog_like"),
    path("<int:pk>/<slug:blog_slug>/", include(comment_patterns)),
    path("<int:pk>/<slug:blog_slug>/", blog_detail_view, name="blog_detail"),
    path("new/", blog_create_view, name="blog_new"),
    path("<str:tag_name>", list_blog_tagged, name="list_blog_tagged"),
    path("", blog_list_view, name="blog_list"),
]
