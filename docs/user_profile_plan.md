# Plan for User Profile Page (Revision 2)

This document outlines the revised plan for creating a modern, responsive, and user-friendly profile page, based on user feedback to avoid tabs and improve the overall UI/UX.

## 1. Analysis

The new direction avoids tabs in favor of a single, scrollable page. This approach is more intuitive for mobile users and provides a cleaner, more modern aesthetic. The design will be minimalist, focusing on clarity and ease of use. We will use cards to group related information into logical sections.

Key principles of the new plan:
- **Single-Column, Scrollable Layout:** All information will be presented in a single, continuous flow, which is ideal for mobile devices.
- **Section-Based Cards:** Information will be organized into distinct cards for "Personal Information" and "Social Media Accounts", creating a clear visual hierarchy.
- **Integrated User Info:** The primary user information (avatar, name) will be presented at the top of the page, not within a card, to give it prominence.
- **Interactive Elements with HTMX:** In-place editing for fields like the mobile number will be retained to ensure a smooth user experience.

## 2. Implementation Plan

The implementation will be broken down into the following steps:

### Step 1: Update the Main Layout

- **File:** `templates/users/profile.html`
- **Action:** Modify the main container to be a single-column layout. The two-column grid will be removed.

### Step 2: Implement the Integrated User Information Header

- **File:** `templates/users/profile.html`
- **Action:** At the top of the page, add a section for the user's primary information.
  - Display the user's avatar (or a placeholder).
  - Display the user's full name and username.
  - Include an "Edit Profile" button.

### Step 3: Create the "Personal Information" Card

- **File:** `templates/users/profile.html`
- **Action:** Below the user information header, create a card for personal details.
  - The card will have a title: "Personal Information".
  - It will contain:
    - The user's email address (read-only).
    - The user's mobile number, with an "Edit" button that uses HTMX to enable in-place editing.

### Step 4: Create the "Social Media Accounts" Card

- **File:** `templates/users/profile.html`
- **Action:** Below the "Personal Information" card, create a card for social media links.
  - The card will have a title: "Social Media Accounts".
  - It will list the user's connected social media accounts with their respective icons.
  - A "Link New Account" button will be included to allow users to add more accounts.

### Step 5: Update HTMX Partials

- **Files:** `templates/users/partials/_edit_mobile_form.html` and `templates/users/partials/_mobile_number_display.html`
- **Action:** Ensure the HTMX partials for editing the mobile number are still compatible with the new layout. The existing partials should work as is, but they will be reviewed to ensure they fit the new design.

### Step 6: Styling and Refinement

- **File:** `templates/users/profile.html`
- **Action:**
  - Apply Tailwind CSS utility classes to ensure a clean and minimalist design with ample whitespace.
  - Use Flowbite component classes for cards and buttons to maintain consistency.
  - Verify the responsiveness of the new layout on different screen sizes.