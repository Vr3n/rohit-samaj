from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from survey.models import (
    SamajMember, SamajMemberMobileNumber, SamajMemberEmail, SamajMemberAddress,
    SamajMemberEducationalQualification, SamajMemberOccupation, SamajMemberIncome,
    Country, State, District, Taluka, City
)

User = get_user_model()

class MultiStageSurveyTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.country = Country.objects.create(name='India', iso='IN', nicename='India', iso3='IND', numcode='356', phone_code=91)
        self.state = State.objects.create(name='Maharashtra', country=self.country)
        self.district = District.objects.create(name='Mumbai', state=self.state)
        self.taluka = Taluka.objects.create(name='Andheri', district=self.district)
        self.city = City.objects.create(name='Mumbai', district=self.district, state=self.state)

    def test_full_survey_flow(self):
        # Stage 1: Personal Info
        response = self.client.post(reverse('survey:personal_info_form'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-01',
            'mobile_numbers-TOTAL_FORMS': 1,
            'mobile_numbers-INITIAL_FORMS': 0,
            'mobile_numbers-MIN_NUM_FORMS': 0,
            'mobile_numbers-MAX_NUM_FORMS': 1000,
            'mobile_numbers-0-mobile_number': '1234567890',
            'emails-TOTAL_FORMS': 1,
            'emails-INITIAL_FORMS': 0,
            'emails-MIN_NUM_FORMS': 0,
            'emails-MAX_NUM_FORMS': 1000,
            'emails-0-email': 'john.doe@example.com',
        })
        member = SamajMember.objects.get(user=self.user)
        self.assertRedirects(response, reverse('survey:address_form', kwargs={'member_id': member.id}))
        self.assertEqual(member.first_name, 'John')
        self.assertEqual(member.mobile_numbers.first().mobile_number, '1234567890')
        self.assertEqual(member.emails.first().email, 'john.doe@example.com')

        # Stage 2: Address Info
        response = self.client.post(reverse('survey:address_form', kwargs={'member_id': member.id}), {
            'perm-flat_no_building': 'P-101',
            'perm-street_landmark': 'Main St',
            'perm-city': self.city.id,
            'perm-district': self.district.id,
            'perm-taluka': self.taluka.id,
            'perm-state': self.state.id,
            'perm-country': self.country.id,
            'perm-pincode': '400001',
            'corr-flat_no_building': 'C-202',
            'corr-street_landmark': 'Side Rd',
            'corr-city': self.city.id,
            'corr-district': self.district.id,
            'corr-taluka': self.taluka.id,
            'corr-state': self.state.id,
            'corr-country': self.country.id,
            'corr-pincode': '400002',
        })
        self.assertRedirects(response, reverse('survey:education_form', kwargs={'member_id': member.id}))
        self.assertEqual(member.addresses.count(), 2)
        perm_address = member.addresses.get(address_type='Permanent')
        corr_address = member.addresses.get(address_type='Correspondence')
        self.assertEqual(perm_address.flat_no_building, 'P-101')
        self.assertEqual(corr_address.flat_no_building, 'C-202')

        # Stage 3: Education Info
        response = self.client.post(reverse('survey:education_form', kwargs={'member_id': member.id}), {
            'educational_qualifications-TOTAL_FORMS': 1,
            'educational_qualifications-INITIAL_FORMS': 0,
            'educational_qualifications-MIN_NUM_FORMS': 0,
            'educational_qualifications-MAX_NUM_FORMS': 1000,
            'educational_qualifications-0-school_name': 'University of Life',
            'educational_qualifications-0-course_name': 'Experience',
            'educational_qualifications-0-university_name': 'World',
            'educational_qualifications-0-city': 'Global',
            'educational_qualifications-0-grade': 'PhD',
        })
        self.assertRedirects(response, reverse('survey:occupation_form', kwargs={'member_id': member.id}))
        self.assertEqual(member.educational_qualifications.count(), 1)
        edu = member.educational_qualifications.first()
        self.assertEqual(edu.school_name, 'University of Life')

        # Stage 4: Occupation Info
        response = self.client.post(reverse('survey:occupation_form', kwargs={'member_id': member.id}), {
            'company_name': 'Acme Corp',
            'designation': 'CEO',
            'occupation_type': 'Business',
            'occupation_name': 'Management',
        })
        self.assertRedirects(response, reverse('survey:income_form', kwargs={'member_id': member.id}))
        self.assertEqual(member.occupations.count(), 1)
        occ = member.occupations.first()
        self.assertEqual(occ.company_name, 'Acme Corp')

        # Stage 5: Income Info
        response = self.client.post(reverse('survey:income_form', kwargs={'member_id': member.id}), {
            'annual_income': '1000000.00',
            'earning_members': 1,
            'other_members': 2,
        })
        self.assertRedirects(response, reverse('survey:survey_sucess'))
        self.assertEqual(member.income.count(), 1)
        inc = member.income.first()
        self.assertEqual(str(inc.annual_income), '1000000.00')

    def test_personal_info_submission_invalid_no_contact(self):
        response = self.client.post(reverse('survey:personal_info_form'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-01',
            'mobile_numbers-TOTAL_FORMS': 0,
            'mobile_numbers-INITIAL_FORMS': 0,
            'mobile_numbers-MIN_NUM_FORMS': 0,
            'mobile_numbers-MAX_NUM_FORMS': 1000,
            'emails-TOTAL_FORMS': 0,
            'emails-INITIAL_FORMS': 0,
            'emails-MIN_NUM_FORMS': 0,
            'emails-MAX_NUM_FORMS': 1000,
        })
        # Should render the same form with errors, not redirect
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "At least one mobile number or email must be provided.")
        self.assertFalse(SamajMember.objects.filter(user=self.user).exists())

    def test_address_submission_invalid(self):
        member = SamajMember.objects.create(
            user=self.user, first_name='John', last_name='Doe', date_of_birth='2000-01-01', added_by=self.user
        )
        SamajMemberMobileNumber.objects.create(member=member, mobile_number='1234567890')

        response = self.client.post(reverse('survey:address_form', kwargs={'member_id': member.id}), {
            'perm-flat_no_building': '', # Invalid: Missing required field
            'perm-street_landmark': 'Main St',
            'perm-city': self.city.id,
            'perm-district': self.district.id,
            'perm-taluka': self.taluka.id,
            'perm-state': self.state.id,
            'perm-country': self.country.id,
            'perm-pincode': '400001',
            'corr-flat_no_building': 'C-202',
            'corr-street_landmark': 'Side Rd',
            'corr-city': self.city.id,
            'corr-district': self.district.id,
            'corr-taluka': self.taluka.id,
            'corr-state': self.state.id,
            'corr-country': self.country.id,
            'corr-pincode': '400002',
        })
        self.assertEqual(response.status_code, 200) # Should render the same form with errors
        self.assertContains(response, "This field is required.")
        self.assertEqual(member.addresses.count(), 0) # No addresses should be saved

    def test_education_submission_invalid_no_grade_or_percentage(self):
        member = SamajMember.objects.create(
            user=self.user, first_name='John', last_name='Doe', date_of_birth='2000-01-01', added_by=self.user
        )
        SamajMemberMobileNumber.objects.create(member=member, mobile_number='1234567890')

        response = self.client.post(reverse('survey:education_form', kwargs={'member_id': member.id}), {
            'educational_qualifications-TOTAL_FORMS': 1,
            'educational_qualifications-INITIAL_FORMS': 0,
            'educational_qualifications-MIN_NUM_FORMS': 0,
            'educational_qualifications-MAX_NUM_FORMS': 1000,
            'educational_qualifications-0-school_name': 'School A',
            'educational_qualifications-0-course_name': 'Course A',
            'educational_qualifications-0-university_name': 'University A',
            'educational_qualifications-0-city': 'City A',
            # Missing both grade and percentage
        })
        self.assertEqual(response.status_code, 200) # Should render the same form with errors
        self.assertContains(response, "Either Grade or Percentage must be provided for Educational Qualification.")
        self.assertEqual(member.educational_qualifications.count(), 0) # No education should be saved

    def test_previous_button_navigation(self):
        # Test navigating from address form to personal info form
        member = SamajMember.objects.create(
            user=self.user, first_name='John', last_name='Doe', date_of_birth='2000-01-01', added_by=self.user
        )
        response = self.client.get(reverse('survey:address_form', kwargs={'member_id': member.id}))
        self.assertEqual(response.status_code, 200) # Should render address form
        
        # Simulate clicking previous button (which is a GET request to personal_info_form)
        response = self.client.get(reverse('survey:personal_info_form'))
        self.assertEqual(response.status_code, 200) # Should render personal info form