# Plan for User Profile Editing

This document outlines the plan for implementing user profile editing functionalities, specifically for mobile number, username, and address.

## 1. Analysis

The goal is to provide users with the ability to edit their mobile number, username, and address directly from their profile page. Each field has different considerations regarding complexity and security, which will influence the chosen implementation approach.

- **Mobile Number:** Already has an existing HTMX-based in-place editing implementation. This approach is suitable and will be maintained.
- **Username:** As a critical identifier and potentially part of authentication, editing the username requires careful handling. A full form submission is preferred to ensure robust validation and security.
- **Address:** An address typically consists of multiple fields (e.g., street, city, state, postal code). A dedicated form for address editing is necessary.

## 2. Implementation Plan

### Step 1: Mobile Number Editing (Review and Refine)

- **Files:** `templates/users/profile.html`, `templates/users/partials/_edit_mobile_form.html`, `templates/users/partials/_mobile_number_display.html`, `users/views.py`, `users/urls.py`
- **Action:** Review the existing HTMX implementation for mobile number editing. Ensure it is fully functional and integrates seamlessly with the new single-column profile page layout. No significant changes are anticipated unless bugs or integration issues are found.

### Step 2: Username Editing

- **Files:** `templates/users/profile.html`, `users/forms.py` (new), `users/views.py`, `users/urls.py`
- **Action:**
  1.  **Create a Django Form:** Develop a new `UsernameChangeForm` in `users/forms.py` that handles username validation.
  2.  **Add a View:** Create a new view in `users/views.py` (e.g., `edit_username`) that renders this form. This view will handle both displaying the form and processing its submission.
  3.  **Update Profile Template:** In `templates/users/profile.html`, add a section for the username. This section will include a button (e.g., "Edit Username") that, when clicked, will open a modal (using Flowbite's modal component) containing the `UsernameChangeForm`.
  4.  **Add URL:** Define a new URL pattern in `users/urls.py` for the `edit_username` view.

### Step 3: Address Editing

- **Files:** `templates/users/profile.html`, `users/forms.py` (new), `users/views.py`, `users/urls.py`, `templates/users/partials/_edit_address_form.html` (new), `templates/users/partials/_address_display.html` (new)
- **Action:**
  1.  **Create a Django Form:** Develop a new `AddressForm` in `users/forms.py` with fields for street, city, state, postal code, and country.
  2.  **Add Views:** Create two new views in `users/views.py`:
      - `edit_address`: Renders the `AddressForm` within `_edit_address_form.html`.
      - `update_address`: Handles the form submission, updates the user's address, and renders `_address_display.html`.
  3.  **Create Partials:**
      - `_edit_address_form.html`: Contains the `AddressForm`.
      - `_address_display.html`: Displays the user's address in a readable format.
  4.  **Update Profile Template:** In `templates/users/profile.html`, add a section for the address. This section will include a button (e.g., "Edit Address") that, when clicked, will use HTMX to swap the display view with `_edit_address_form.html`. Upon submission, `_address_display.html` will be swapped back.
  5.  **Add URLs:** Define new URL patterns in `users/urls.py` for the `edit_address` and `update_address` views.

### Step 4: Styling and Integration

- **Files:** All modified templates and forms.
- **Action:** Apply Tailwind CSS utility classes and Flowbite components to all new forms and partials to ensure a consistent look and feel with the rest of the profile page. Ensure all HTMX interactions are smooth and provide appropriate user feedback.
