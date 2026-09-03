# Qualitative Research Gaps & User Research Protocol

This document explicitly identifies the boundaries of observational clickstream event data and outlines the qualitative user research protocols required to validate behavioral assumptions before final engineering rollout.

---

## 1. What Quantitative Clickstream Data Cannot Tell Us

While ShopSphere's event-level clickstream captures *what* actions users took and *when* they took them, quantitative logs cannot directly measure customer cognitive states, mental models, or off-site behaviors:

```text
+-------------------------------------------------------------------+-------------------------------------------------------------------+
| WHAT CLICKSTREAM DATA MEASURES (QUANTITATIVE)                     | WHAT CLICKSTREAM DATA CANNOT MEASURE (QUALITATIVE GAPS)           |
+-------------------------------------------------------------------+-------------------------------------------------------------------+
| • 45s median mobile address dwell time                            | • Whether the user experienced typing fatigue or validation errors|
| • 27.5% shipping drop-off on sub-$40 carts                        | • Whether the customer perceived shipping as too slow or too costly|
| • 41.3% checkout rate after invalid promo error                   | • Where the user acquired the code (e.g., Honey, RetailMeNot, ad) |
| • 25.9% immediate session exit after payment decline              | • Whether the user distrusted the site or was confused by message |
| • Monotonic conversion decay with 7+ product views                | • Whether the user was comparison shopping or lost in navigation  |
| • 48% conversion gap between new and returning visitors          | • Whether first-time buyers lacked brand trust vs saved profiles  |
+-------------------------------------------------------------------+-------------------------------------------------------------------+
```

---

## 2. Qualitative Research Protocol by Journey Stage

### Gap 1: Mobile Address Form Input Friction (`PROB-01`)
- **Core Qualitative Question:** *What specific elements of the mobile address form create user hesitation, input errors, or form abandonment?*
- **Proposed Research Methodology:** **Moderated Usability Lab Testing ($N = 12$ smartphone participants)**
  - *Setup:* Screen-recorded task where participants purchase an item using mobile web on iOS and Android devices while thinking aloud.
  - *Key Focus:* Observe zoom shifts on field focus, keyboard switching friction, autofill prompt interaction, and error tooltip clarity.

---

### Gap 2: Shipping Fee Threshold Perception (`PROB-02`)
- **Core Qualitative Question:** *Do customers perceive the $\$75$ free shipping threshold as attainable, and what price point triggers delivery fee abandonment?*
- **Proposed Research Methodology:** **Exit-Intent Micro-Surveys ($N = 500$ responses)**
  - *Setup:* 1-question un-intrusive survey triggered when a sub-$\$75$ cart user moves cursor to close the checkout tab: *"What was the main reason you didn't complete your order today?"*
  - *Options:* (A) Shipping cost higher than expected, (B) Delivery too slow, (C) Just browsing / price comparing, (D) Other.

---

### Gap 3: Payment Error Comprehension & Trust (`PROB-03`)
- **Core Qualitative Question:** *How do customers interpret card decline messages, and what barriers prevent them from switching to Digital Wallets?*
- **Proposed Research Methodology:** **Session Replay Video Audit ($N = 100$ anonymized failed checkout sessions)**
  - *Setup:* Qualitative review of session replay heatmaps and mouse/touch trajectories immediately following a `payment_failed` event.
  - *Key Focus:* Measure rage clicks, cursor thrashing, and whether users attempted to edit card numbers vs looking for alternate payment buttons.

---

### Gap 4: Promo Code Sourcing & Rejection Reactance (`PROB-04`)
- **Core Qualitative Question:** *Where do customers find invalid promo codes, and why does rejection prompt funnel exit?*
- **Proposed Research Methodology:** **Customer Discovery Interviews ($N = 15$ recent cart abandoners)**
  - *Setup:* 15-minute exploratory interviews with users who abandoned cart after entering an invalid promo code.
  - *Key Focus:* Understand coupon extension usage (Honey, CapitalOne Shopping) and whether users expect store-wide discounts before buying.

---

### Gap 5: First-Time Buyer Trust & Guest Checkout Preferences (`PROB-05`)
- **Core Qualitative Question:** *What trust signals (security badges, reviews, payment icons) most effectively reassure first-time buyers during checkout?*
- **Proposed Research Methodology:** **Unmoderated Card Sorting & Tree Testing ($N = 60$ participants)**
  - *Setup:* Test checkout step arrangements and trust badge placements to evaluate perceived checkout safety and ease of use.
