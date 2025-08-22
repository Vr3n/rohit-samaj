# The Survey Form

Survey form is to know what is the state of community members.\

- What is the qualifications, income range, most clustered area?

- First go through the @survey/models, @survey/forms, and @survey/views
- then go through the @templates/
- Plan the Multistage survey form accordingly.
- Should not be over engineered, but also should not be too unmaintainable.

## The form

We have broken down the form into parts.

- This is multi stage forms, but we save every stage to model in @survey/models.py
- Each step is independent, only SamajMember object is important as the data is related to member.
- Added By should be the logged in `request.user` so we know which user has added the samaj member.

1. Samaj Member personal info
   - first_name: required.
   - last_name: required.
   - father_name: optional
   - mother_name: optional
   - date_of_birth: required

   ** Either mobile_number or email should be present **
   - mobile_number: required
   - alternate_mobile_number: optional
   - email: optional
   - alternate_email: optional

2. Samaj Member Address Info

There will be 2 types of addresses: Permanent, and Correspondance.

- Permanent: Where the Samaj member has own house, or stays permanently.
- Correspondance: Where the samaj member lives temporarily, shifted for job, etc.

- A checkbox "same address as permanent." will copy the corr to perm.

- The fields are:
  - corr_flat_no_building: required
  - corr_street_landmark: optional
  - corr_city: required
  - corr_taluka: required
  - corr_district: required
  - corr_state: required
  - corr_country: required
  - corr_pincode: required

  - perm_flat_no_building: required
  - perm_street_landmark: optional
  - perm_city: required
  - perm_taluka: required
  - perm_district: required
  - perm_state: required
  - perm_country: required
  - perm_pincode: required

3. Samaj Member Educational Qualification.

- The fields are:
  - school_name: required
  - course_name: required
  - university_name: required
  - education_city: required

  ** Either grade or percentage should be present **
  - grade: optional
  - percentage: optional

  - description: optional

4. Samaj Member Occupational Details.

- The fields are:
  - company_name: required
  - designation: required
  - occupation_type: optional
  - occupation_name: optional
  - company_city: optional

5. Samaj Member Income Details

- The fields are:
  - annual_income: required
  - earning_members: required
  - other_members: required

---

I have already implemented survey form, but it is not good.
Improve the forms.

We need different Django forms for survey:

1. The Personal Info Section

Models used: SamajMemberMobileNumber, SamajMemberEmail, SamajMember

- SamajMemberPersonalInfoForm:
  - This section saves samaj member's personal info like mentioned above.
  - We need Inline formset mobile_number, and email.

Also add appropriate validations.

2. Address Info section

Models used: SamajMemberAddress

- SamajMemberAddressForm:
  - The section saved samaj member's address.
  - Have a checkbox which says "same address as Correspondance." which will copy the values to permanent address.

3. Educational Qualification section

Models used: SamajMemberEducationalQualification

- SamajMemberEducationalQualificationForm
  - Section saves educational qualifications of a member.
  - inline formset which enables us to add multiple qualifications.

4. Occupational Details

Models used: SamajMemberOccupation

- SamajMemberOccupationForm
  - Saving the Occupational details of a member.

5. Income Details

Models used: SamajMemberIncome

- SamajMemberIncomeForm
  - SAving the income and how many people are bread winners.
