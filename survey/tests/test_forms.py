from django.test import TestCase
from django.contrib.auth import get_user_model
from survey.forms import (
    SamajMemberPersonalInfoForm, SamajMemberMobileNumberForm, SamajMemberEmailForm,
    SamajMemberAddressForm, SamajMemberEducationalQualificationForm,
    SamajMemberOccupationForm, SamajMemberIncomeForm,
    SamajMemberMobileNumberFormSet, SamajMemberEmailFormSet,
    SamajMemberEducationalQualificationFormSet
)
from survey.models import (
    SamajMember, SamajMemberMobileNumber, SamajMemberEmail, SamajMemberAddress,
    SamajMemberEducationalQualification, SamajMemberOccupation, SamajMemberIncome,
    Country, State, District, Taluka, City
)
import datetime

User = get_user_model()

class FormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.country = Country.objects.create(name='India', iso='IN', nicename='India', iso3='IND', numcode='356', phone_code=91)
        self.state = State.objects.create(name='Maharashtra', country=self.country)
        self.district = District.objects.create(name='Mumbai', state=self.state)
        self.taluka = Taluka.objects.create(name='Andheri', district=self.district)
        self.city = City.objects.create(name='Mumbai', district=self.district, state=self.state)

    def test_samaj_member_personal_info_form_valid(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-01',
        }
        form = SamajMemberPersonalInfoForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_samaj_member_personal_info_form_invalid(self):
        form_data = {
            'first_name': '', # Missing required field
            'last_name': 'Doe',
            'date_of_birth': '2000-01-01',
        }
        form = SamajMemberPersonalInfoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_samaj_member_mobile_number_form_valid(self):
        form_data = {'mobile_number': '1234567890'}
        form = SamajMemberMobileNumberForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_samaj_member_mobile_number_form_invalid(self):
        form_data = {'mobile_number': '123'} # Too short
        form = SamajMemberMobileNumberForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mobile_number', form.errors)

        form_data = {'mobile_number': 'abcdefghij'} # Non-digits
        form = SamajMemberMobileNumberForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mobile_number', form.errors)

    def test_samaj_member_email_form_valid(self):
        form_data = {'email': 'test@example.com'}
        form = SamajMemberEmailForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_samaj_member_email_form_invalid(self):
        form_data = {'email': 'invalid-email'}
        form = SamajMemberEmailForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_samaj_member_address_form_valid(self):
        form_data = {
            'flat_no_building': 'A-101',
            'street_landmark': 'Near Park',
            'city': self.city.id,
            'district': self.district.id,
            'taluka': self.taluka.id,
            'state': self.state.id,
            'country': self.country.id,
            'pincode': '400001',
        }
        form = SamajMemberAddressForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_samaj_member_address_form_invalid(self):
        form_data = {
            'flat_no_building': '', # Missing required field
            'street_landmark': 'Near Park',
            'city': self.city.id,
            'district': self.district.id,
            'taluka': self.taluka.id,
            'state': self.state.id,
            'country': self.country.id,
            'pincode': '400001',
        }
        form = SamajMemberAddressForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('flat_no_building', form.errors)

    def test_samaj_member_educational_qualification_form_valid(self):
        form_data_grade = {
            'school_name': 'ABC School',
            'course_name': 'SSC',
            'university_name': 'Maharashtra Board',
            'city': 'Mumbai',
            'grade': 'A+',
        }
        form = SamajMemberEducationalQualificationForm(data=form_data_grade)
        self.assertTrue(form.is_valid(), form.errors)

        form_data_percentage = {
            'school_name': 'ABC School',
            'course_name': 'SSC',
            'university_name': 'Maharashtra Board',
            'city': 'Mumbai',
            'percentage': '90.50',
        }
        form = SamajMemberEducationalQualificationForm(data=form_data_percentage)
        self.assertTrue(form.is_valid(), form.errors)

    def test_samaj_member_educational_qualification_form_invalid(self):
        form_data = {
            'school_name': 'ABC School',
            'course_name': 'SSC',
            'university_name': 'Maharashtra Board',
            'city': 'Mumbai',
            # Missing both grade and percentage
        }
        form = SamajMemberEducationalQualificationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors) # Custom validation error

    def test_samaj_member_occupation_form_valid(self):
        form_data = {
            'company_name': 'XYZ Corp',
            'designation': 'Software Engineer',
            'occupation_type': 'Service',
            'occupation_name': 'IT',
        }
        form = SamajMemberOccupationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_samaj_member_occupation_form_invalid(self):
        form_data = {
            'company_name': '', # Missing required field
            'designation': 'Software Engineer',
            'occupation_type': 'Service',
            'occupation_name': 'IT',
        }
        form = SamajMemberOccupationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_samaj_member_income_form_valid(self):
        form_data = {
            'annual_income': '500000.00',
            'earning_members': 2,
            'other_members': 3,
        }
        form = SamajMemberIncomeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_samaj_member_income_form_invalid(self):
        form_data = {
            'annual_income': '', # Missing required field
            'earning_members': 2,
            'other_members': 3,
        }
        form = SamajMemberIncomeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('annual_income', form.errors)

    def test_mobile_number_formset(self):
        member = SamajMember.objects.create(
            first_name='Test', last_name='Member', user=self.user, added_by=self.user
        )
        formset_data = {
            'mobile_numbers-TOTAL_FORMS': 2,
            'mobile_numbers-INITIAL_FORMS': 0,
            'mobile_numbers-MIN_NUM_FORMS': 0,
            'mobile_numbers-MAX_NUM_FORMS': 1000,
            'mobile_numbers-0-mobile_number': '1112223334',
            'mobile_numbers-1-mobile_number': '5556667778',
        }
        formset = SamajMemberMobileNumberFormSet(formset_data, instance=member)
        self.assertTrue(formset.is_valid(), formset.errors)
        instances = formset.save()
        self.assertEqual(len(instances), 2)
        self.assertEqual(member.mobile_numbers.count(), 2)

    def test_email_formset(self):
        member = SamajMember.objects.create(
            first_name='Test', last_name='Member', user=self.user, added_by=self.user
        )
        formset_data = {
            'emails-TOTAL_FORMS': 2,
            'emails-INITIAL_FORMS': 0,
            'emails-MIN_NUM_FORMS': 0,
            'emails-MAX_NUM_FORMS': 1000,
            'emails-0-email': 'test1@example.com',
            'emails-1-email': 'test2@example.com',
        }
        formset = SamajMemberEmailFormSet(formset_data, instance=member)
        self.assertTrue(formset.is_valid(), formset.errors)
        instances = formset.save()
        self.assertEqual(len(instances), 2)
        self.assertEqual(member.emails.count(), 2)

    def test_educational_qualification_formset(self):
        member = SamajMember.objects.create(
            first_name='Test', last_name='Member', user=self.user, added_by=self.user
        )
        formset_data = {
            'educational_qualifications-TOTAL_FORMS': 2,
            'educational_qualifications-INITIAL_FORMS': 0,
            'educational_qualifications-MIN_NUM_FORMS': 0,
            'educational_qualifications-MAX_NUM_FORMS': 1000,
            'educational_qualifications-0-school_name': 'School A',
            'educational_qualifications-0-course_name': 'Course A',
            'educational_qualifications-0-university_name': 'University A',
            'educational_qualifications-0-city': 'City A',
            'educational_qualifications-0-grade': 'A',
            'educational_qualifications-1-school_name': 'School B',
            'educational_qualifications-1-course_name': 'Course B',
            'educational_qualifications-1-university_name': 'University B',
            'educational_qualifications-1-city': 'City B',
            'educational_qualifications-1-percentage': '85.00',
        }
        formset = SamajMemberEducationalQualificationFormSet(formset_data, instance=member)
        self.assertTrue(formset.is_valid(), formset.errors)
        instances = formset.save()
        self.assertEqual(len(instances), 2)
        self.assertEqual(member.educational_qualifications.count(), 2)
