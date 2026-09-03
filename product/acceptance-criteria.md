# ShopSphere Acceptance Criteria Specification

This document provides formal, testable acceptance criteria in standard **Given / When / Then** format for all functional requirements across the checkout journey.

---

## 1. Address Entry Acceptance Criteria (`FR-ADDR-101`, `FR-ADDR-102`, `FR-ADDR-103`)

### AC-ADDR-01: Address Autocomplete Dynamic Dropdown
- **Given** a customer is on the `address_entry` checkout step on a mobile or desktop device,
- **When** the customer enters 3 or more characters into the street address field (e.g., *"123 Main"*),
- **Then** the system shall display a dropdown list of up to 5 matching verified postal addresses within $\le 200\text{ms}$.

### AC-ADDR-02: Autocomplete Selection & Field Population
- **Given** an address suggestion list is displayed,
- **When** the customer taps or clicks on a suggested address,
- **Then** the system shall automatically populate the `Street Address`, `City`, `State`, and `Postal Code` fields and close the suggestion dropdown without clearing any user-entered apartment/suite numbers.

### AC-ADDR-03: Manual Address Entry & Fallback
- **Given** the customer prefers to type their address manually or the autocomplete API is unreachable,
- **When** the customer continues typing without selecting a suggestion or clicks outside the dropdown,
- **Then** the system shall allow free-form text entry and validate the fields upon `onBlur` against standard postal format rules.

### AC-ADDR-04: Mobile Numeric Keypad Display
- **Given** a customer is using a mobile browser,
- **When** the customer focuses on the `Phone Number` or `Postal Code` input fields,
- **Then** the mobile operating system shall render a dedicated numeric telephone/digit keypad (`inputmode="tel"` or `inputmode="numeric"`).

---

## 2. Shipping Threshold Acceptance Criteria (`FR-SHIP-201`, `FR-SHIP-202`)

### AC-SHIP-01: Progress Bar Calculation for Sub-$75 Carts
- **Given** a customer has items in their cart totaling $\$52.50$ (below the $\$75.00$ threshold),
- **When** the customer views the cart drawer or cart page,
- **Then** the interface shall display a visual progress bar filled to $70.0\%$ ($52.50 / 75.00$) with the text: *"Add $22.50 more for FREE Shipping!"*.

### AC-SHIP-02: Threshold Qualification Confirmation
- **Given** a customer has items in their cart totaling $\$75.00$ or greater,
- **When** the cart drawer or checkout shipping page renders,
- **Then** the progress bar shall be 100% filled in green with the message: *"You've unlocked FREE Shipping!"* and the calculated shipping fee at step 2 shall be $\$0.00$.

### AC-SHIP-03: 1-Click Threshold Add-On Addition
- **Given** a customer's cart value is between $\$50.00$ and $\$74.99$,
- **When** the customer taps the `+ Add to Cart` button on a recommended add-on item in the cart carousel,
- **Then** the item shall be added to the cart asynchronously, the subtotal and free shipping progress bar shall update instantly within $\le 250\text{ms}$, and the user shall remain on the cart view without page reloads.

---

## 3. Payment Recovery Acceptance Criteria (`FR-PAY-301`, `FR-PAY-302`)

### AC-PAY-01: Soft Decline Recovery Modal Display
- **Given** a customer submits a payment authorization that returns a soft decline error (e.g., `ERR_GATEWAY_TIMEOUT`, `ERR_3DS_AUTH_FAILED`, `ERR_INSUFFICIENT_FUNDS`),
- **When** the gateway decline response is received,
- **Then** the checkout system shall retain all entered shipping and contact data and display a focused modal explaining the issue with prominent 1-click options to switch to Apple Pay, Google Pay, or enter a new card.

### AC-PAY-02: 1-Click Alternative Payment Method Execution
- **Given** the recovery modal is displayed after a declined debit card attempt,
- **When** the customer taps the `Apple Pay` / `Google Pay` button,
- **Then** the system shall launch the native wallet authorization sheet pre-populated with the order amount, and upon authorization, complete the purchase and advance directly to the `order_completed` confirmation screen.

---

## 4. Promo Code Validation Acceptance Criteria (`FR-PROMO-401`, `FR-PROMO-402`)

### AC-PROMO-01: Collapsible Drawer Expansion & Entry
- **Given** a customer is viewing the cart summary,
- **When** the customer taps the *"+ Have a promo code?"* link,
- **Then** the input field and `Apply` button shall expand smoothly with automatic cursor focus.

### AC-PROMO-02: Friendly Invalid Promo Error & Continuity
- **Given** a customer submits an invalid or expired promo code,
- **When** the validation response returns an error (`ERR_INVALID_PROMO`),
- **Then** the system shall display an inline helper text: *"This promo code is expired or invalid for these items"* in amber/neutral styling without page refresh, maintain the full cart contents, and keep the `Proceed to Checkout` button active and unobstructed.

---

## 5. Guest Checkout Acceptance Criteria (`FR-CUST-501`, `FR-CUST-502`)

### AC-CUST-01: Frictionless Guest Checkout Initiation
- **Given** an unauthenticated visitor clicks `Checkout`,
- **When** the checkout page loads,
- **Then** the system shall directly present the email and shipping address fields without requiring account login or password setup.

### AC-CUST-02: Post-Purchase 1-Click Account Creation
- **Given** a guest customer successfully completes an order,
- **When** the `order_completed` confirmation page renders,
- **Then** the interface shall display an optional account creation card with a single `Create Password` field and `Save Account` button that transfers all order details to the new account profile upon submission.
