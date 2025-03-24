from django.contrib.auth.models import User
from django.dispatch import receiver

from allauth.account.signals import user_signed_up
from django.http import HttpRequest

from users.models import UserProfile


@receiver(user_signed_up)
def create_user_profile(request: HttpRequest, user: User, **kwargs):
    """
    Creates a user profile after first-time login via OAuth.
    """

    _ = UserProfile.objects.get_or_create(user=user)
