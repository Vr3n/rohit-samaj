from django import forms
from django.core.validators import RegexValidator

from survey.models import (City, Country, District,
                           SamajMember, State,
                           SamajMemberMobileNumber, SamajMemberIncome,
                           SamajMemberEmail,
                           SamajMemberEducationalQualification,
                           SamajMemberAddress, SamajMemberOccupation)


class AcceptTermsForm(forms.Form):
    caste_terms = forms.BooleanField(required=True)
    accept_terms = forms.BooleanField(required=True)


class SamajSurveyForm(forms.Form):
    # Personal Details
    first_name = forms.CharField(
        label="First Name", required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    father_name = forms.CharField(required=False, max_length=100)
    mother_name = forms.CharField(required=False, max_length=100)
    guardian_name = forms.CharField(required=False, max_length=250)

    # Contact Information
    mobile_number = forms.CharField(
        required=True,
        max_length=10,
        min_length=10,
        validators=[RegexValidator(
            r'^\d{10}$', 'Enter a valid 10-digit mobile number.')]
    )
    email = forms.EmailField(required=False)
    alternate_mobile_number = forms.CharField(
        required=False,
        max_length=10,
        min_length=10,
        validators=[RegexValidator(
            r'^\d{10}$', 'Enter a valid 10-digit mobile number.')]
    )
    alternate_email = forms.EmailField(required=False)

    # Address Details.
    corr_flat_no_building = forms.CharField(required=False, max_length=100)
    corr_street_landmark = forms.CharField(required=False, max_length=100)
    corr_city = forms.CharField(required=True, max_length=100)
    corr_taluka = forms.CharField(required=True, max_length=100)
    corr_district = forms.CharField(required=True, max_length=100)
    corr_state = forms.CharField(required=True, max_length=100)
    corr_country = forms.CharField(required=True, max_length=100)
    corr_pincode = forms.CharField(
        required=True,
        max_length=6,
        min_length=6,
        validators=[RegexValidator(
            r'^\d{6}$', 'Enter a valid 6-digit pincode.')]
    )

    # Permanent Address Details.
    perm_flat_no_building = forms.CharField(required=False, max_length=100)
    perm_street_landmark = forms.CharField(required=False, max_length=100)
    perm_city = forms.CharField(required=True, max_length=100)
    perm_taluka = forms.CharField(required=True, max_length=100)
    perm_district = forms.CharField(required=True, max_length=100)
    perm_state = forms.CharField(required=True, max_length=100)
    perm_country = forms.CharField(required=True, max_length=100)
    perm_pincode = forms.CharField(
        required=True,
        max_length=6,
        min_length=6,
        validators=[RegexValidator(
            r'^\d{6}$', 'Enter a valid 6-digit pincode.')]
    )

    # Educational Qualification
    school_name = forms.CharField(required=False, max_length=100)
    course_name = forms.CharField(required=False, max_length=100)
    university_name = forms.CharField(required=False, max_length=100)
    education_city = forms.CharField(required=False, max_length=100)
    grade = forms.CharField(required=False, max_length=50)
    percentage = forms.DecimalField(
        required=False, max_digits=5, decimal_places=2, min_value=0, max_value=100)

    # Occupational Details
    company_name = forms.CharField(required=False, max_length=100)
    designation = forms.CharField(required=False, max_length=100)
    occupation_type = forms.ChoiceField(choices=[("Business", "Business"), ("Service", "Service"), (
        "Self Employed", "Self Employed"),
        ("Government Job", "Government Job"), ("Farmer", "Farmer")],
        required=False)
    occupation_name = forms.CharField(required=False, max_length=100)
    company_city = forms.CharField(required=False, max_length=100)

    # Income Details
    annual_income = forms.DecimalField(
        required=True, max_digits=10, decimal_places=2)
    earning_members = forms.IntegerField(required=True, min_value=0)
    other_members = forms.IntegerField(required=True, min_value=0)

    def save(self) -> None:
        # Extracting the cleaned data.
        cleaned_data = self.cleaned_data

        if self.cleaned_data['corr_country']:
            corr_country, _ = Country.objects.get_or_create(
                name=cleaned_data['corr_country'])

        if self.cleaned_data['corr_state']:
            corr_state, _ = State.objects.get_or_create(
                name=cleaned_data['corr_state'])

        if self.cleaned_data['corr_district']:
            corr_district, _ = District.objects.get_or_create(
                name=cleaned_data['corr_district'])

        if self.cleaned_data['corr_city']:
            corr_city, _ = City.objects.get_or_create(
                name=cleaned_data['corr_city'])

        if self.cleaned_data['perm_country']:
            perm_country, _ = Country.objects.get_or_create(
                name=cleaned_data['perm_country'])

        if self.cleaned_data['perm_state']:
            perm_state, _ = State.objects.get_or_create(
                name=cleaned_data['perm_state'])

        if self.cleaned_data['perm_district']:
            perm_district, _ = District.objects.get_or_create(
                name=cleaned_data['perm_district'])

        if self.cleaned_data['perm_city']:
            perm_city, _ = City.objects.get_or_create(
                name=cleaned_data['perm_city'])

        # Create the samaj member entry.
        member = SamajMember.objects.create(
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            father_name=cleaned_data['father_name'],
            mother_name=cleaned_data['mother_name'],
        )

        # Samaj Member Mobile Number.
        SamajMemberMobileNumber.objects.create(
            member=member,
            mobile_number=self.cleaned_data['mobile_number']
        )

        if self.cleaned_data['alternate_mobile_number']:
            SamajMemberMobileNumber.objects.create(
                member=member,
                mobile_number=self.cleaned_data['alternate_mobile_number']
            )

        # Samaj Member Email Address.
        SamajMemberEmail.objects.create(
            member=member,
            mobile_number=self.cleaned_data['email']
        )

        if self.cleaned_data['alternate_email']:
            SamajMemberEmail.objects.create(
                member=member,
                mobile_number=self.cleaned_data['alternate_email']
            )

        # Correspondance Address.
        SamajMemberAddress.objects.create(
            member=member,
            flat_no_building=cleaned_data.get('corr_flat_no_building'),
            street_landmark=cleaned_data.get('corr_street_landmark', ''),
            city=corr_city,
            taluka=corr_taluka,
            district=corr_district,
            state=corr_state,
            country=corr_country,
            pincode=cleaned_data['corr_pincode']
        )

        # Permanent Address.
        SamajMemberAddress.objects.create(
            member=member,
            flat_no_building=cleaned_data.get('perm_flat_no_building'),
            street_landmark=cleaned_data.get('perm_street_landmark', ''),
            city=perm_city,
            taluka=perm_taluka,
            district=perm_district,
            state=perm_state,
            country=perm_country,
            pincode=cleaned_data['perm_pincode']
        )

        # Educational Qualification.
        SamajMemberEducationalQualification.objects.create(
            member=member,
            school_name=cleaned_data['school_name'],
            course_name=cleaned_data['course_name'],
            university_name=cleaned_data['university_name'],
            education_city=cleaned_data['education_city'],
            grade=cleaned_data.get('grade', ''),
            percentage=cleaned_data.get('percentage', '')
        )

        # Income Details.
        SamajMemberIncome.objects.create(
            member=member,
            annual_income=cleaned_data['annual_income'],
            earning_members=cleaned_data['earning_members'],
            other_members=cleaned_data['other_members']
        )

        # samaj member occupation details.
        SamajMemberOccupation.objects.create(
            member=member,
            company_name=cleaned_data['company_name'],
            designation=cleaned_data['designation'],
            occupation_type=cleaned_data['occupation_type'],
            occupation_name=cleaned_data['occupation_name'],
        )
