# Plan for Address Form with Dynamic Dropdowns

This document outlines the plan to update the address form in the survey to have dynamic dropdowns for State, District, and Taluka, with the default country set to India.

## 1. Update `survey/views.py`

In the `get` method of the `SamajMemberAddressView`:

- Fetch the `Country` object for "India".
- Set the `initial` value for the `country` field in both `corr_address_form` and `perm_address_form` to the ID of the "India" object.
- Fetch the list of states for India and pass it to the template context. This will be used to populate the initial state dropdown.

## 2. Update `survey/forms.py`

In the `SamajMemberAddressForm`:

- The `__init__` method will be updated to correctly handle the initial data for the `country` field.
- The querysets for `state`, `district`, and `taluka` will be empty initially. They will be populated dynamically using HTMX.

## 3. Update `templates/survey/address_form.html`

- The dropdowns for Country, State, District, and Taluka will be updated with HTMX attributes.
- **Country Dropdown**:
  - On change, it will trigger a `GET` request to an HTMX view to fetch the states for the selected country.
  - The response will replace the content of the state dropdown.
- **State Dropdown**:
  - On change, it will trigger a `GET` request to an HTMX view to fetch the districts for the selected state.
  - The response will replace the content of the district dropdown.
- **District Dropdown**:
  - On change, it will trigger a `GET` request to an HTMX view to fetch the talukas for the selected district.
  - The response will replace the content of the taluka dropdown.
- The `corr_` and `perm_` prefixes for the forms will be handled in the HTMX views and templates to ensure the correct dropdowns are updated.

## 4. Create HTMX Templates

- New templates will be created in `templates/survey/hx/` to render the `<option>` tags for the dropdowns.
- A generic `_options.html` template will be created to be reused for all dropdowns.
