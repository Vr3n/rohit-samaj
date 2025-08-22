from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UsernameChangeForm, AddressForm
from survey.models import SamajMemberAddress, SamajMember


@login_required
def user_profile_view(request: HttpRequest) -> HttpResponse:
    """Renders the user profile page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered user profile page.
    """
    user_profile_obj: UserProfile = UserProfile.objects.get(user=request.user)

    return render(request, "users/profile.html", {
        "user_profile": user_profile_obj
    })


@login_required
def edit_mobile_number(request: HttpRequest) -> HttpResponse:
    """Renders the form to edit the user's mobile number.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered mobile number edit form partial.
    """
    user_profile_obj: UserProfile = UserProfile.objects.get(user=request.user)
    return render(request, "users/partials/_edit_mobile_form.html", {
        "user_profile": user_profile_obj
    })


@login_required
def update_profile(request: HttpRequest) -> HttpResponse:
    """Handles the update of the user's profile information.

    Currently supports updating the mobile number.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the updated mobile number display partial
                      or an HTTP 405 status if the request method is not POST.
    """
    if request.method == "POST":
        user_profile_obj: UserProfile = UserProfile.objects.get(user=request.user)
        phone_number = request.POST.get("phone_number")
        user_profile_obj.phone_number = phone_number
        user_profile_obj.save()
        return render(request, "users/partials/_mobile_number_display.html", {
            "user_profile": user_profile_obj
        })
    return HttpResponse(status=405)


@login_required
def edit_username(request: HttpRequest) -> HttpResponse:
    """Handles the editing of the user's username.

    Displays a form for username change and processes its submission.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the username edit modal or redirects to profile on success.
    """
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.save()
            messages.success(request, "Your username was successfully updated!")
            return redirect('users:profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UsernameChangeForm(user=request.user)

    return render(request, 'users/partials/_edit_username_modal.html', {
        'form': form
    })


@login_required
def edit_address(request: HttpRequest) -> HttpResponse:
    """Renders the form to edit the user's address.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered address edit form partial.
    """
    samaj_member = get_object_or_404(SamajMember, user=request.user)
    address, created = SamajMemberAddress.objects.get_or_create(member=samaj_member)
    form = AddressForm(instance=address)
    return render(request, "users/partials/_edit_address_form.html", {
        "form": form,
        "address": address
    })


@login_required
def update_address(request: HttpRequest) -> HttpResponse:
    """Handles the update of the user's address information.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the updated address display partial
                      or an HTTP 405 status if the request method is not POST.
    """
    samaj_member = get_object_or_404(SamajMember, user=request.user)
    address, created = SamajMemberAddress.objects.get_or_create(member=samaj_member)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return render(request, "users/partials/_address_display.html", {
                "address": address
            })
        else:
            return render(request, "users/partials/_edit_address_form.html", {
                "form": form,
                "address": address
            })
    return HttpResponse(status=405)
