# Product Problem → Candidate Intervention Mapping Matrix

This document maps the empirical problem diagnoses identified in Phase 4 (`PROB-01` through `PROB-06`) to structured candidate product interventions, articulating the underlying behavioral rationale, boundary conditions, and experimental validation required.

---

### PROB-01: Mobile Address Form Input Friction
- **Journey Stage:** Checkout — Address Entry (`address_entry` $\to$ `shipping_view`).
- **Observed Problem:** Mobile shoppers exhibit a statistically significant $-7.89\text{ pp}$ deficit in address completion ($79.18\%$ vs $87.07\%$ on Desktop) and spend $+21.6\%$ longer completing the step (Median $45\text{s}$ vs $37\text{s}$).
- **Empirical Evidence:** Multivariate Adjusted $\text{OR} = 0.5704$ ($95\%\text{ CI: } 0.5232–0.6220, p < 10^{-36}$). Mobile-attributable excess loss accounts for **$1,043.7$ sessions** ($28.8\%$ of total address stage dropouts).
- **Affected Segment:** Mobile checkout shoppers ($13,239$ sessions, $66.4\%$ of checkout traffic).
- **Business Consequence:** Primary checkout drop-off bottleneck suppressing mobile conversion.
- **Confidence Level:** **High.**
- **Open Product Question:** Is the friction caused by multi-field typing burden, strict postal code formatting, or lack of autofill integration?
- **Candidate Intervention Approach A (Primary):** **Address Autocomplete & Express Geolocation Lookup.** Integrate Google Places / Postal Code auto-fill API that populates City, State, and Postal Code upon typing 3 characters.
- **Candidate Intervention Approach B (Alternative):** **1-Click Mobile Express Checkout.** Introduce native Apple Pay / Google Pay / ShopPay buttons directly on the Cart and initial Checkout screen to bypass address entry entirely.
- **Why These Interventions Address Observed Friction:** Reduces mobile typing from 8+ manual fields to a single tap or verified selection, directly mitigating touchscreen input fatigue.
- **What The Interventions Do NOT Prove:** Does not prove whether mobile users abandon due to security hesitation vs input burden.
- **Validation Required:** A/B test comparing Address Autocomplete vs Control on mobile address progression and completion rate.

---

### PROB-02: Delivery Fee Sticker Shock on Sub-$75 Baskets
- **Journey Stage:** Checkout — Shipping Review (`shipping_view` $\to$ `payment_select`).
- **Observed Problem:** Shipping review drop-off rises sharply from $6.16\%$ for free-shipping orders ($\ge \$75$) to $19.73\%$ for $\$40\text{--}\$60$ carts and $27.49\%$ for sub-$\$40$ carts.
- **Empirical Evidence:** Logistic regression demonstrates $\text{OR} = 1.4927$ per $+10\text{ pp}$ increase in `shipping_cost / cart_value` ($p < 10^{-100}$). Near-threshold carts ($\$60\text{--}\$74.99$) exhibit elevated backtracking ($9.29\%$).
- **Affected Segment:** Sub-$\$75$ checkout sessions ($6,475$ sessions reaching shipping review).
- **Business Consequence:** $1,567$ lost checkout sessions among sub-threshold shoppers.
- **Confidence Level:** **High.**
- **Open Product Question:** Will upfront shipping threshold communication increase basket building (AOV) and reduce abandonment without eroding margin?
- **Candidate Intervention Approach A (Primary):** **Dynamic Free Shipping Progress Bar & Cart Upsell.** Real-time progress bar on cart drawer and product pages ("Add $\$14.50$ for FREE Shipping") with 1-click add-on recommendations.
- **Candidate Intervention Approach B (Alternative):** **Tiered Low-Cost Economy Shipping.** Introduce an unbundled, slower economy shipping tier ($\$3.99$) for sub-$\$40$ orders alongside standard delivery.
- **Why These Interventions Address Observed Friction:** Empowers shoppers to bridge the threshold gap through item additions rather than encountering an unexpected delivery charge at step 2 of checkout.
- **What The Interventions Do NOT Prove:** Does not prove customer willingness to wait longer for economy shipping or product catalog add-on affinity.
- **Validation Required:** A/B test measuring cart-to-purchase conversion, AOV, and net shipping margin contribution.

---

### PROB-03: Unrecovered Payment Declines & Gateway Timeouts
- **Journey Stage:** Checkout — Payment Authorization (`payment_attempt` $\to$ `payment_success` / `order_completed`).
- **Observed Problem:** $47.72\%$ of checkout sessions encountering payment declines permanently abandon without completing an order.
- **Empirical Evidence:** $857$ sessions encounter payment declines ($6.52\%$ decline rate). Net Banking ($11.64\%$) and Debit Cards ($8.72\%$) suffer the highest failure rates. $25.9\%$ of users exit immediately upon first decline. $409$ prospective orders permanently lost.
- **Affected Segment:** High-intent shoppers attempting payment ($857$ failed sessions).
- **Business Consequence:** Permanent loss of $409$ highly qualified transactions ($>\$45,000$ unrealized GMV).
- **Confidence Level:** **High.**
- **Open Product Question:** Does rigid error messaging discourage recovery, and will automated fallback options prevent immediate tab closure?
- **Candidate Intervention Approach A (Primary):** **Smart Decline Recovery Modal & 1-Click Alternate Payment Prompt.** When a card or bank decline occurs, present a friendly, contextual modal explaining the issue and offering 1-click fallback to Digital Wallets (Apple Pay/Google Pay) or saved backup methods.
- **Candidate Intervention Approach B (Alternative):** **Automated Invisible Gateway Fallback.** Dynamically re-route failed gateway timeout transactions through a secondary acquiring bank before showing user errors.
- **Why These Interventions Address Observed Friction:** Replaces dead-end red error banners with actionable recovery pathways while keeping checkout state and cart contents intact.
- **What The Interventions Do NOT Prove:** Does not bypass legitimate bank-level insufficient funds or anti-fraud blocks.
- **Validation Required:** A/B test measuring payment failure recovery rate and subsequent session conversion.

---

### PROB-04: Pre-Checkout Promotional Code Rejection Attrition
- **Journey Stage:** Shopping Cart — Promo Application (`add_to_cart` $\to$ `promo_applied` $\to$ `checkout_start`).
- **Observed Problem:** Cart sessions triggering invalid promo code errors advance to checkout at only $41.25\%$ vs $62.57\%$ for baseline carts ($-21.32\text{ pp}$ deficit).
- **Empirical Evidence:** $\chi^2 = 244.1, p < 10^{-50}$; final session conversion drops from $40.32\%$ to $26.56\%$. $836$ cart sessions lost pre-checkout.
- **Affected Segment:** Price-sensitive coupon seekers ($1,423$ cart sessions).
- **Business Consequence:** Pre-checkout cart abandonment and coupon-hunting off-site distraction.
- **Confidence Level:** **Moderate-High (Subject to Selection Bias).**
- **Open Product Question:** Does a prominent coupon input box trigger off-site coupon hunting, and does inline error feedback soften disappointment?
- **Candidate Intervention Approach A (Primary):** **Collapsible Promo Code Drawer & Inline Available Deals.** De-emphasize empty text field into a subtle link ("Have a promo code?") and display a curated dropdown of eligible, verified store promotions.
- **Candidate Intervention Approach B (Alternative):** **Auto-Apply Best Coupon at Cart Creation.** Automatically evaluate and apply the highest-value qualifying discount to the cart, eliminating manual code entry.
- **Why These Interventions Address Observed Friction:** Prevents users from leaving the checkout funnel to search for unverified codes and eliminates negative rejection feedback.
- **What The Interventions Do NOT Prove:** Does not eliminate underlying price sensitivity among coupon hunters.
- **Validation Required:** A/B test measuring cart-to-checkout initiation rate, coupon redemption rate, and gross margin.

---

### PROB-05: First-Time Visitor Guest Checkout Onboarding Barrier
- **Journey Stage:** Multi-Stage Checkout Funnel (`cart` $\to$ `address` $\to$ `shipping` $\to$ `purchase`).
- **Observed Problem:** New visitors convert at $9.08\%$ vs $13.46\%$ for returning customers ($+48.2\%$ gap), with elevated dropout at address entry ($20.21\%$).
- **Empirical Evidence:** Multivariate Adjusted $\text{OR} = 1.5518$ ($p < 10^{-100}$) for returning customers.
- **Affected Segment:** New visitor traffic ($62.18\%$ of total traffic, $74,612$ sessions).
- **Business Consequence:** Substantial monetization drag across the majority of inbound acquisition traffic.
- **Confidence Level:** **High (Observational Pattern).**
- **Open Product Question:** Will streamlined guest checkout with optional post-purchase password creation reduce initial form hesitation?
- **Candidate Intervention Approach A (Primary):** **Frictionless Guest Checkout with Post-Purchase Account Creation.** Default to guest checkout with zero password requirements upfront; offer 1-click account creation on the Order Confirmation page.
- **Candidate Intervention Approach B (Alternative):** **Social Login / Federated Single Sign-On (Google/Apple).** Provide 1-tap sign-in at checkout start to instantly pre-populate name and email.
- **Why These Interventions Address Observed Friction:** Removes upfront commitment and account creation friction, aligning first-time checkout speed with returning customer baselines.
- **What The Interventions Do NOT Prove:** Does not measure brand trust or perceived payment security.
- **Validation Required:** A/B test measuring new visitor checkout completion rate and post-purchase account creation rate.

---

### PROB-06: High-Ticket Cart Payment Friction & Limit Declines
- **Journey Stage:** Checkout — Payment Selection & Authorization.
- **Observed Problem:** Orders $>\$300$ experience higher payment dropout ($8.4\%$ vs $4.8\%$) and higher credit card decline rates ($7.52\%$).
- **Empirical Evidence:** $\chi^2 = 23.29, p < 0.0001$; credit card declines on large orders skewed by card limits and bank risk challenges.
- **Affected Segment:** High-GMV checkout sessions ($1,279$ payment dropouts, top-tier $> \$300$).
- **Business Consequence:** Disproportionate loss of high-margin revenue.
- **Confidence Level:** **Moderate-High.**
- **Open Product Question:** Will prominent installment/BNPL options and split-payment capabilities resolve card limit friction?
- **Candidate Intervention Approach A:** **Prominent BNPL Installment Display (e.g., "4 payments of $\$75$").** Surface installment pricing on product pages, cart, and payment selection.
- **Candidate Intervention Approach B:** **Split-Card Payment Option.** Allow customers to distribute high-ticket orders across two payment instruments.
- **Why These Interventions Address Observed Friction:** Bypasses single-card transaction limits and reduces immediate cash outlay hesitation.
- **What The Interventions Do NOT Prove:** Does not measure consumer credit qualification approval rates.
- **Validation Required:** A/B test on high-ticket cart conversion and BNPL adoption share.
