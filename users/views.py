from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserProfile

# Create your views here.


@login_required
def user_profile_view(request: HttpRequest) -> HttpResponse:

    user_profile_obj: UserProfile = UserProfile.objects.get(user=request.user)

    return render(request, "users/profile.html", {
        "user_profile": user_profile_obj
    })
