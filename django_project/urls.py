from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from accounts.views import profile_update

urlpatterns = [
    path("admin/", admin.site.urls),
    path("update/", profile_update, name="profile_update"),
    path("accounts/", include("allauth.urls")),
    path("blogs/", include("blogs.urls")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
