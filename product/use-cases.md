# ShopSphere Product Use Cases

This document details the primary, alternative, and exception user interaction flows across the key checkout journey touchpoints.

---

## UC-01: Mobile Address Autocomplete Completion

- **Use Case ID:** `UC-01`
- **Related Problem ID:** `PROB-01` (Mobile Address Form Friction)
- **Related Requirements:** `BR-ADDR-01`, `FR-ADDR-101`, `FR-ADDR-102`, `NFR-PERF-01`
- **Actor:** Mobile Web Shopper
- **Trigger:** User taps the `Street Address` field on the mobile `address_entry` step.
- **Preconditions:** User has added $\ge 1$ product to cart and clicked `Checkout`.
- **Main Flow:**
  1. User types the first 3 characters of their street address (e.g., *"742"*).
  2. System queries the autocomplete service and renders up to 5 verified address suggestions below the input box within $200\text{ms}$.
  3. User taps their verified address from the suggestion list.
  4. System automatically populates `Street Address`, `City`, `State`, and `Postal Code`.
  5. User enters their apartment/unit number (if applicable) and taps `Continue to Shipping`.
  6. System validates the complete address and transitions to `shipping_view`.
- **Alternative Flow (Manual Entry):**
  - At step 3, user ignores the dropdown suggestions and types their full address manually.
  - System validates fields `onBlur` and allows progression.
- **Exception Flow (API Unavailable):**
  - At step 2, autocomplete API times out ($>1.5\text{s}$). System gracefully suppresses the suggestion box and allows standard manual text entry with standard regex validation.
- **Postconditions:** Valid address is stored in the session payload; user successfully reaches `shipping_view`.

---

## UC-02: Free Shipping Threshold Awareness & Cart Building

- **Use Case ID:** `UC-02`
- **Related Problem ID:** `PROB-02` (Sub-$75 Shipping Fee Sticker Shock)
- **Related Requirements:** `BR-SHIP-01`, `FR-SHIP-201`, `FR-SHIP-202`
- **Actor:** Shopper with cart value $<\$75.00$
- **Trigger:** User adds an item to cart or opens the cart drawer.
- **Preconditions:** Cart contains at least one item with total value $<\$75.00$.
- **Main Flow:**
  1. User opens the cart drawer with a current subtotal of $\$58.00$.
  2. Interface displays the free shipping progress bar filled to $77.3\%$ with text: *"Add $17.00 more for FREE Shipping!"*.
  3. Interface presents a carousel of 3 recommended add-on items priced between $\$10.00$ and $\$20.00$.
  4. User clicks `+ Add to Cart` on an accessory priced at $\$18.00$.
  5. System updates the subtotal to $\$76.00$, renders the progress bar at 100% green checkmark (*"FREE Shipping Unlocked!"*), and removes delivery charges.
  6. User clicks `Proceed to Checkout` with zero shipping sticker shock.
- **Alternative Flow (User Ignores Add-Ons):**
  - User proceeds with $\$58.00$ cart; shipping review clearly displays the calculated standard delivery fee prior to payment.
- **Postconditions:** Higher cart value achieved; reduced probability of shipping review abandonment.

---

## UC-03: Payment Decline Recovery via Digital Wallet

- **Use Case ID:** `UC-03`
- **Related Problem ID:** `PROB-03` (Unrecovered Payment Declines)
- **Related Requirements:** `BR-PAY-01`, `FR-PAY-301`, `FR-PAY-302`
- **Actor:** Checkout Shopper attempting payment
- **Trigger:** User clicks `Place Order`, and the acquiring bank returns a soft decline (e.g., `ERR_GATEWAY_TIMEOUT` or `ERR_3DS_AUTH_FAILED`).
- **Preconditions:** User has completed address and shipping steps and submitted a payment authorization.
- **Main Flow:**
  1. Payment gateway authorization fails with a soft decline code.
  2. System captures the failure event, retains all checkout details, and renders the Smart Recovery Modal.
  3. Modal explains: *"Your bank was unable to complete authorization. Would you like to try 1-click Apple Pay / Google Pay or use another card?"*.
  4. User taps `Apple Pay` / `Google Pay`.
  5. Native wallet biometric prompt appears; user confirms authorization.
  6. Transaction captures successfully; system advances to `order_completed` confirmation screen.
- **Alternative Flow (Retry Same Card):**
  - User checks card details, corrects CVV/expiration, and clicks `Retry Payment`.
- **Exception Flow (Hard Decline / Stolen Card):**
  - Gateway returns `ERR_FRAUD_BLOCK`. System displays prompt to enter an entirely different payment method.
- **Postconditions:** Qualified customer transaction recovered; order completed.

---

## UC-04: Promo Code Entry & Inline Error Recovery

- **Use Case ID:** `UC-04`
- **Related Problem ID:** `PROB-04` (Promo Code Rejection Attrition)
- **Related Requirements:** `BR-PROMO-01`, `FR-PROMO-401`, `FR-PROMO-402`, `FR-PROMO-403`
- **Actor:** Value-conscious Shopper in Cart
- **Trigger:** User clicks *"+ Have a promo code?"* link in cart drawer.
- **Preconditions:** User has $\ge 1$ item in cart.
- **Main Flow:**
  1. User expands promo drawer and types a code (e.g., *"SUMMER20"*).
  2. User clicks `Apply`.
  3. System sends asynchronous validation request.
  4. Validation succeeds; interface displays green badge (*"-$15.00 applied"*) and updates subtotal.
  5. User advances to checkout.
- **Alternative Flow (Invalid Promo Code):**
  - User enters an expired third-party coupon code.
  - System returns `ERR_INVALID_PROMO`.
  - Interface displays friendly inline message: *"This code is expired or invalid for these items"* and displays a list of active store deals (*"Use WELCOME10 for 10% off"*).
  - User applies the valid store deal or proceeds to checkout without frustration.
- **Postconditions:** Cart contents maintained; user proceeds to checkout without abandoning.

---

## UC-05: Frictionless First-Time Guest Checkout & Post-Purchase Onboarding

- **Use Case ID:** `UC-05`
- **Related Problem ID:** `PROB-05` (New Customer Guest Barrier)
- **Related Requirements:** `BR-CUST-01`, `FR-CUST-501`, `FR-CUST-502`
- **Actor:** First-time Shopper
- **Trigger:** User clicks `Proceed to Checkout`.
- **Preconditions:** User has no existing active session account.
- **Main Flow:**
  1. User enters checkout and is presented immediately with Email and Address fields (no password prompt).
  2. User completes address with autocomplete, selects shipping, and pays via credit card or digital wallet.
  3. System captures payment and redirects to `order_completed` screen.
  4. Confirmation screen displays order summary and an onboarding card: *"Save your information for 1-click checkout on your next order"*.
  5. User enters a password and taps `Save Account`.
  6. System creates registered account profile linked to the order history and customer ID.
- **Alternative Flow (User Skips Account Creation):**
  - User ignores account creation and receives standard email order receipt as a guest.
- **Postconditions:** Order placed with minimum upfront friction; optional account created post-conversion.
