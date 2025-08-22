from django import forms
from django.core.validators import RegexValidator
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

from survey.models import (
    City, Country, District, Taluka,
    SamajMember, State,
    SamajMemberMobileNumber, SamajMemberIncome,
    SamajMemberEmail,
    SamajMemberEducationalQualification,
    SamajMemberAddress, SamajMemberOccupation
)

# Define common form widget attributes for Flowbite styling
text_input_attrs = {
    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
}
date_input_attrs = {
    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
}
checkbox_attrs = {
    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
}


class AcceptTermsForm(forms.Form):
    caste_terms = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs=checkbox_attrs))
    accept_terms = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs=checkbox_attrs))


class SamajMemberPersonalInfoForm(forms.ModelForm):
    mobile_number = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit mobile number.')],
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs)
    )
    alternate_mobile_number = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit mobile number.')],
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs)
    )
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs=text_input_attrs))
    alternate_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs=text_input_attrs))

    class Meta:
        model = SamajMember
        fields = [
            'first_name', 'last_name', 'father_name', 'mother_name',
            'date_of_birth', 'guardian_name',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs=text_input_attrs),
            'last_name': forms.TextInput(attrs=text_input_attrs),
            'father_name': forms.TextInput(attrs=text_input_attrs),
            'mother_name': forms.TextInput(attrs=text_input_attrs),
            'guardian_name': forms.TextInput(attrs=text_input_attrs),
            'date_of_birth': forms.DateInput(attrs={**date_input_attrs, 'datepicker': True, 'datepicker-format': 'dd/mm/yyyy', 'data-datepicker-autohide': 'true'}, format='%d/%m/%Y'),
        }

    def clean(self):
        cleaned_data = super().clean()
        mobile_number = cleaned_data.get('mobile_number')
        email = cleaned_data.get('email')

        if not mobile_number and not email:
            raise ValidationError("At least one contact method (mobile number or email) must be provided.")
        return cleaned_data


class SamajMemberAddressForm(forms.ModelForm):
    is_permanent_same_as_correspondence = forms.BooleanField(
        required=False,
        label="Same as Correspondence Address",
        widget=forms.CheckboxInput(attrs=checkbox_attrs)
    )

    class Meta:
        model = SamajMemberAddress
        fields = [
            'flat_no_building', 'street_landmark', 'city', 'district',
            'taluka', 'state', 'country', 'pincode'
        ]
        widgets = {
            'flat_no_building': forms.TextInput(attrs=text_input_attrs),
            'street_landmark': forms.TextInput(attrs=text_input_attrs),
            'pincode': forms.TextInput(attrs=text_input_attrs),
            'country': forms.Select(attrs=text_input_attrs),
            'state': forms.Select(attrs=text_input_attrs),
            'district': forms.Select(attrs=text_input_attrs),
            'taluka': forms.Select(attrs=text_input_attrs),
            'city': forms.Select(attrs=text_input_attrs),
        }


class SamajMemberEducationalQualificationForm(forms.ModelForm):
    class Meta:
        model = SamajMemberEducationalQualification
        fields = [
            'school_name', 'course_name', 'university_name', 'city',
            'grade', 'percentage', 'description'
        ]
        widgets = {
            'school_name': forms.TextInput(attrs=text_input_attrs),
            'course_name': forms.TextInput(attrs=text_input_attrs),
            'university_name': forms.TextInput(attrs=text_input_attrs),
            'city': forms.TextInput(attrs=text_input_attrs),
            'grade': forms.TextInput(attrs=text_input_attrs),
            'percentage': forms.NumberInput(attrs=text_input_attrs),
            'description': forms.Textarea(attrs={**text_input_attrs, 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get('grade')
        percentage = cleaned_data.get('percentage')

        if not grade and not percentage:
            raise ValidationError(
                "Either Grade or Percentage must be provided for Educational Qualification."
            )
        return cleaned_data


SamajMemberEducationalQualificationFormSet = inlineformset_factory(
    SamajMember,
    SamajMemberEducationalQualification,
    form=SamajMemberEducationalQualificationForm,
    extra=1,
    can_delete=True,
)


class SamajMemberOccupationForm(forms.ModelForm):
    class Meta:
        model = SamajMemberOccupation
        fields = [
            'company_name', 'designation', 'occupation_type',
            'occupation_name', 'company_city'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs=text_input_attrs),
            'designation': forms.TextInput(attrs=text_input_attrs),
            'occupation_type': forms.Select(attrs=text_input_attrs),
            'occupation_name': forms.TextInput(attrs=text_input_attrs),
            'company_city': forms.TextInput(attrs=text_input_attrs),
        }


class SamajMemberIncomeForm(forms.ModelForm):
    class Meta:
        model = SamajMemberIncome
        fields = [
            'annual_income', 'earning_members', 'other_members'
        ]
        widgets = {
            'annual_income': forms.NumberInput(attrs=text_input_attrs),
            'earning_members': forms.NumberInput(attrs=text_input_attrs),
            'other_members': forms.NumberInput(attrs=text_input_attrs),
        }