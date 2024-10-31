from django.urls import path
from .views import profile_update

urlpatterns = [
    path("profile/update/", profile_update, name="profile_update"),
]
