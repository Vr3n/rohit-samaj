from django.db import models
from django.utils import timezone

# Location Models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso = models.CharField(max_length=100, unique=True)
    nicename = models.CharField(max_length=100)
    iso3 = models.CharField(max_length=100)
    numcode = models.CharField(max_length=100)
    phone_code = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self) -> str:
        return f"{self.name} - {self.country.name}"


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='districts')

    def __str__(self) -> str:
        return f"{self.name} - {self.state.name}"


class Taluka(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='talukas')

    def __str__(self) -> str:
        return f"{self.name} - {self.district.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 related_name='cities', blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,
                              blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

# Main Samaj Member Model


class SamajMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.father_name} {self.mother_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name

# Contact Information


class SamajMemberMobileNumber(models.Model):
    member = models.ForeignKey(
        SamajMember, on_delete=models.CASCADE, related_name='mobile_numbers')
    # Add validators for digits only
    mobile_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.mobile_number} - {self.member.full_name}"


class SamajMemberEmail(models.Model):
    member = models.ForeignKey(
        SamajMember, on_delete=models.CASCADE, related_name='emails')
    # Add validators for digits only
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.email} - {self.member.full_name}"


# Address Information


class SamajMemberAddress(models.Model):
    member = models.ForeignKey(
        SamajMember, on_delete=models.CASCADE, related_name='addresses')
    flat_no_building = models.CharField(max_length=100)
    street_landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=True, null=True)
    taluka = models.ForeignKey(
        Taluka, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=True, null=True)
    pincode = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Education Information


class SamajMemberEducationalQualification(models.Model):
    member = models.ForeignKey(
        SamajMember, on_delete=models.CASCADE, related_name='educational_qualifications')
    school_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    grade = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Occupational Details


class SamajMemberOccupation(models.Model):
    member = models.ForeignKey(
        SamajMember, on_delete=models.CASCADE, related_name='occupations')
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    occupation_type = models.CharField(
        max_length=20,
        choices=[
            ('Business', 'Business'),
            ('Service', 'Service'),
            ('Self Employed', 'Self Employed'),
            ('Government Job', 'Government Job')
        ]
    )
    occupation_name = models.CharField(max_length=100)
    company_city = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Income Details


class SamajMemberIncome(models.Model):
    member = models.ForeignKey(
        SamajMember, on_delete=models.CASCADE, related_name='income')
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    earning_members = models.PositiveIntegerField()
    other_members = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
