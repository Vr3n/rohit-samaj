from django.contrib.auth.models import User
from django.dispatch import receiver

from allauth.account.signals import user_signed_up
from django.http import HttpRequest

from survey.models import (
    SamajMember, SamajMemberMobileNumber, SamajMemberEmail)
from users.models import UserProfile


@receiver(user_signed_up)
def create_user_profile(request: HttpRequest, user: User, **kwargs):
    """
    Creates a user profile after first-time login via OAuth.
    """

    profile_obj: UserProfile

    profile_obj, _ = UserProfile.objects.get_or_create(user=user)

    social_login = kwargs.get("sociallogin")

    # Extract avtar URL from social account.
    avatar_url = None

    if social_login:
        provider = social_login.account.provider

        if provider == "google":
            avatar_url = social_login.account.extra_data.get("picture")
        elif provider == "facebook":
            avatar_url = f"https://graph.facebook.com/{sociallogin.account.uid}/picture?type=large"

    # Create or update the user profile.
    if avatar_url:
        profile_obj.avatar = avatar_url
        profile_obj.save()
