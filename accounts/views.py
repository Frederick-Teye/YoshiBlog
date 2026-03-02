from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import ProfileUpdateForm
from .models import CustomUser


@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # change redirect to profile page in the future.
            return redirect("home")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "account/profile_update.html", {"form": form})


def profile_detail_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    user_blogs = profile_user.blog_set.all().order_by("-date")

    return render(
        request,
        "account/profile_detail.html",
        {"profile_user": profile_user, "user_blogs": user_blogs},
    )
