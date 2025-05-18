from django.forms import ModelForm

from users.models import UserProfile


class ProfileMobileEditForm(ModelForm[UserProfile]):

    class Meta:
        model = UserProfile
        fields: list[str] = [
            "phone_number"
        ]
