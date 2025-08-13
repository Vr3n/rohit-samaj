import logging
from django.contrib.auth.models import User
from django.db import transaction
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.http import HttpRequest
from survey.models import SamajMember, SamajMemberEmail
from users.models import UserProfile

logger = logging.getLogger(__name__)


@receiver(user_signed_up)
def create_user_profile(request: HttpRequest, user: User, **kwargs):
    """
    Creates a user profile after first-time login via OAuth.
    It also creates a SamajMember if one does not exist for the email.
    """
    try:
        with transaction.atomic():
            profile_obj, _ = UserProfile.objects.get_or_create(user=user)

            # Check if a SamajMember with the user's email already exists.
            email_qs = SamajMemberEmail.objects.filter(email=user.email)
            sm_obj = None

            if email_qs.exists():
                # If email exists, get the first associated SamajMember.
                sm_obj = email_qs.first().member
            else:
                # If no SamajMember with this email, create a new one.
                sm_obj = SamajMember.objects.create(
                    user=user,
                    first_name=user.first_name or "",
                    last_name=user.last_name or "",
                )
                SamajMemberEmail.objects.create(member=sm_obj, email=user.email)

            # If a SamajMember is found or created and is not linked to a user, link it.
            if sm_obj and not sm_obj.user:
                sm_obj.user = user
                sm_obj.save()

            # Extract avatar URL from social account.
            social_login = kwargs.get("sociallogin")
            avatar_url = None
            if social_login:
                provider = social_login.account.provider
                if provider == "google":
                    avatar_url = social_login.account.extra_data.get("picture")
                elif provider == "facebook":
                    avatar_url = f"https://graph.facebook.com/{social_login.account.uid}/picture?type=large"

            # Create or update the user profile with the avatar.
            if avatar_url:
                profile_obj.avatar = avatar_url
                profile_obj.save()

    except Exception as e:
        logger.error(
            f"Error in create_user_profile signal for user {user.email}: {e}",
            exc_info=True,
        )
