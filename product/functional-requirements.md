# ShopSphere Functional Requirements Specification (FRS)

This document translates the approved Business Requirements into testable, unambiguous functional specifications across all key checkout journey stages.

---

## 1. Address Entry & Mobile Optimization (`BR-ADDR-01`)

### FR-ADDR-101: Real-Time Address Autocomplete API
- **Description:** When a user types in the Street Address field, the system shall query an address validation service (e.g., Google Places / Postal Service API) after $3$ characters and display up to $5$ matching address suggestions in a mobile-optimized dropdown.
- **Interaction:** Selecting an address suggestion shall automatically populate `Street Address`, `City`, `State/Province`, `Postal Code`, and `Country`.
- **Manual Fallback:** Users shall retain the ability to dismiss suggestions and enter/edit address fields manually.

### FR-ADDR-102: Mobile Keyboard & Viewport Optimization
- **Description:** The mobile web interface shall map specific HTML5 `inputmode` and `autocomplete` attributes to every form field:
  - `name`: `autocomplete="name"`, `type="text"`
  - `phone`: `autocomplete="tel"`, `inputmode="tel"`, `type="tel"`
  - `postal_code`: `autocomplete="postal-code"`, `inputmode="numeric"`, `type="text"`
  - `email`: `autocomplete="email"`, `inputmode="email"`, `type="email"`
- **Viewport Behavior:** The mobile view shall ensure input focus does not cause viewport zoom disruption (minimum font size $16\text{px}$).

### FR-ADDR-103: Inline Field Validation & Error Highlighting
- **Description:** Form field validation shall occur `onBlur` (when the user leaves a field) rather than exclusively `onSubmit`.
- **Error Behavior:** If a field contains an invalid format (e.g., malformed postal code), display a clear, specific helper message beneath the field with red border highlighting without clearing existing valid text.

---

## 2. Shipping Threshold Communication (`BR-SHIP-01`)

### FR-SHIP-201: Dynamic Free Shipping Progress Bar
- **Description:** The shopping cart drawer, cart page, and shipping review stage shall render an interactive visual progress bar displaying the user's progress toward the $\$75.00$ free-shipping threshold:
  - When `cart_value < $75.00`: Display progress bar filled to `(cart_value / 75.0) * 100%` with text: *"Add $[75.00 - cart_value] more to unlock FREE Shipping!"*
  - When `cart_value >= $75.00`: Display 100% filled progress bar with text: *"You've unlocked FREE Shipping!"* with a green checkmark icon.

### FR-SHIP-202: 1-Click Threshold Add-On Recommendations
- **Description:** When `cart_value` is between $\$50.00$ and $\$74.99$, the cart interface shall display a curated carousel of $3\text{--}4$ low-cost catalog add-on items priced between $\$5.00$ and $\$20.00$ with a 1-click `+ Add to Cart` button.

### FR-SHIP-203: Pre-Checkout Shipping Fee Transparency
- **Description:** The cart summary shall explicitly indicate estimated shipping fees or free shipping qualification *prior* to checkout initiation, eliminating surprise price increases at step 2.

---

## 3. Payment Decline Recovery & Gateway Fallback (`BR-PAY-01`)

### FR-PAY-301: Decline Cause Classification & Soft/Hard Error Mapping
- **Description:** When a payment gateway error response is received, the system shall classify the error code into Soft Declines vs Hard Declines:
  - **Soft Declines** (`ERR_GATEWAY_TIMEOUT`, `ERR_3DS_AUTH_FAILED`, `ERR_BANK_DECLINE`, `ERR_INSUFFICIENT_FUNDS`): Eligible for instant retry and alternative payment switching.
  - **Hard Declines** (`ERR_CARD_STOLEN`, `ERR_FRAUD_BLOCK`): Prompt for an entirely new payment method.

### FR-PAY-302: Smart Recovery Modal & Alternative APM Prompt
- **Description:** Upon a soft decline, the system shall suppress generic error banners and display a focused modal:
  - Clear, non-technical explanation (e.g., *"Your card issuer was unable to authorize this transaction. Please retry or choose a different payment method."*)
  - 1-Click buttons for available Digital Wallets (Apple Pay, Google Pay, PayPal) pre-configured with the user's order total.
  - Retain all previously entered shipping and contact details without requiring page reloads.

### FR-PAY-303: Automated Gateway Timeout Retry
- **Description:** For `ERR_GATEWAY_TIMEOUT`, the backend payment orchestration service shall automatically execute one invisible background retry to an alternate gateway endpoint within $3.0$ seconds before surfacing an error to the user.

---

## 4. Promo Code Interface & Validation (`BR-PROMO-01`)

### FR-PROMO-401: Collapsible Promo Code Drawer
- **Description:** The promo code entry field in the cart shall be rendered as a collapsed text link: *"+ Have a promo code?"*. Clicking the link expands the input box and `Apply` button.

### FR-PROMO-402: Asynchronous Inline Promo Validation
- **Description:** When a user submits a promo code, validation shall execute via an asynchronous AJAX request without refreshing the page or clearing cart contents.
- **Success Response:** Display green confirmation badge with exact discount amount deducted from the subtotal.
- **Failure Response:** If invalid (`ERR_INVALID_PROMO`), display friendly inline message: *"This promo code is expired or not applicable to your items"* alongside a link to *View Available Deals*.

### FR-PROMO-403: Eligible Deals Carousel
- **Description:** The expanded promo drawer shall list currently active, eligible store promotions (e.g., *"WELCOME10 - 10% off your first order"*) with a 1-click `Apply` button.

---

## 5. Guest Checkout & Account Continuity (`BR-CUST-01`)

### FR-CUST-501: Default Guest Checkout Path
- **Description:** Initiating checkout (`checkout_start`) shall immediately route users to the email/shipping form without displaying a mandatory login or account creation wall.

### FR-CUST-502: Post-Purchase 1-Click Account Creation
- **Description:** On the `order_completed` confirmation page, display a streamlined account creation prompt: *"Save your details for 1-click checkout next time"*, requiring only a single password entry. All name, email, and shipping address data from the completed order shall be automatically transferred to the new account.
