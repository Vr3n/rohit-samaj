from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from users.models import UserProfile
from survey.models import SamajMemberAddress


class ProfileMobileEditForm(ModelForm):
    class Meta:
        model = UserProfile
        fields: list[str] = ["phone_number"]


class UsernameChangeForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["username"].initial = self.user.username

    def clean_username(self):
        username = self.cleaned_data["username"]
        if (
            self.user
            and User.objects.filter(username=username).exclude(pk=self.user.pk).exists()
        ):
            raise forms.ValidationError("This username is already taken.")
        return username


class AddressForm(ModelForm):
    class Meta:
        model = SamajMemberAddress
        fields = [
            "flat_no_building",
            "street_landmark",
            "city",
            "district",
            "taluka",
            "state",
            "country",
            "pincode",
        ]
