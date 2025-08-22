## Revised Phase 3: Refactor `survey/views.py` (Separate Views for Each Stage) (Completed)

- [x] **3.1 Create `SamajMemberCreateView` (for Personal Info)**:
  - [x] This view will handle the creation of the `SamajMember` object and its associated `SamajMemberMobileNumber` and `SamajMemberEmail` instances.
  - [x] Upon successful submission, it will redirect to the next stage, passing the `SamajMember.id` as a URL parameter.
- [x] **3.2 Create `SamajMemberAddressView`**:
  - [x] This view will take `SamajMember.id` as a URL parameter.
  - [x] It will handle the creation/update of `SamajMemberAddress` objects (permanent and correspondence).
  - [x] Upon successful submission, it will redirect to the next stage, passing the `SamajMember.id`.
- [x] **3.3 Create `SamajMemberEducationView`**:
  - [x] This view will take `SamajMember.id` as a URL parameter.
  - [x] It will handle the creation/update of `SamajMemberEducationalQualification` objects using a formset.
  - [x] Upon successful submission, it will redirect to the next stage, passing the `SamajMember.id`.
- [x] **3.4 Create `SamajMemberOccupationView`**:
  - [x] This view will take `SamajMember.id` as a URL parameter.
  - [x] It will handle the creation/update of `SamajMemberOccupation` object.
  - [x] Upon successful submission, it will redirect to the next stage, passing the `SamajMember.id`.
- [x] **3.5 Create `SamajMemberIncomeView`**:
  - [x] This view will take `SamajMember.id` as a URL parameter.
  - [x] It will handle the creation/update of `SamajMemberIncome` object.
  - [x] Upon successful submission, it will redirect to the success page.
- [x] **3.6 Update `survey/urls.py`**:
  - [x] Define separate URL patterns for each new view, including the `SamajMember.id` parameter where necessary.
- [x] **3.7 Update HTMX views**: Ensure `hx_perm_district_select`, `hx_corr_district_select`, `hx_corr_taluka_select`, `hx_perm_taluka_select`, `add_mobile_number_form`, `add_email_form`, `add_education_form` are still compatible or adjusted as needed.

## Revised Phase 4: Refactor `templates/` (Separate Templates for Each Section) (Completed)

- [x] **4.1 Create `survey/personal_info_form.html`**:
  - [x] This template will render `SamajMemberPersonalInfoForm`, `SamajMemberMobileNumberFormSet`, and `SamajMemberEmailFormSet`.
  - [x] It will have a "Next" button that submits to `SamajMemberCreateView`.
- [x] **4.2 Create `survey/address_form.html`**:
  - [x] This template will render `SamajMemberAddressForm` (for both permanent and correspondence).
  - [x] It will have "Previous" and "Next" buttons.
- [x] **4.3 Create `survey/education_form.html`**:
  - [x] This template will render `SamajMemberEducationalQualificationFormSet`.
  - [x] It will have "Previous" and "Next" buttons.
- [x] **4.4 Create `survey/occupation_form.html`**:
  - [x] This template will render `SamajMemberOccupationForm`.
  - [x] It will have "Previous" and "Next" buttons.
- [x] **4.5 Create `survey/income_form.html`**:
  - [x] This template will render `SamajMemberIncomeForm`.
  - [x] It will have "Previous" and "Submit" buttons.
- [x] **4.6 Update `survey/form.html`**: This file will likely become a wrapper or be removed, depending on how the "illusion" of a multi-stage form is maintained. For now, I will assume it will be replaced by the individual stage templates.

## Phase 5: Testing and Verification (To be updated)

- [x] Write unit tests for each new form and formset to ensure correct validation and data handling.
- [x] Write integration tests for the complete multi-stage survey form flow.
- [ ] Perform manual testing in the browser to verify functionality and user experience. (Pending user action)
