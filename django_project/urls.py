from django.conf import settings
import importlib.util
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

if settings.DEBUG and importlib.util.find_spec("debug_toolbar") is not None:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
