from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

# Create your views here.


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
