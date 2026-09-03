# ShopSphere Product Problem Statements: Checkout & Journey Friction Diagnostics

This document formalizes the empirical findings from Phases 3 and 4 into standardized, evidence-backed Product Problem Statements to guide Phase 5 experimentation and optimization.

---

### PROB-01: Mobile Address Form Input Friction
- **User Journey Stage:** Checkout — Address Entry (`address_entry` $\to$ `shipping_view`).
- **Observed Problem:** Mobile shoppers exhibit a statistically significant deficit in completing the address entry stage compared to desktop shoppers.
- **Empirical Evidence:** In a multivariate logistic regression controlling for customer maturity, mobile users exhibit an overall Adjusted $\text{OR} = 0.5704$ ($95\%\text{ CI: } 0.5232–0.6220, p < 10^{-36}$) of passing address entry relative to desktop users (in an interaction model: $\text{OR} = 0.6074$ for new visitors, $\text{OR} = 0.5200$ for returning customers). Mobile address dwell times are $+21.6\%$ longer (Median $45\text{s}$ vs $37\text{s}$). Mobile-attributable excess loss accounts for **$1,043.7$ abandoned sessions** ($28.8\%$ of total address stage losses).
- **Affected Segment:** Mobile checkout shoppers ($66.4\%$ of address starters, $13,239$ sessions).
- **Business Consequence:** Substantial checkout attrition at the initial data-entry stage, suppressing mobile monetization on ShopSphere's largest traffic channel.
- **Confidence Level:** **High.**
- **Open Product Questions:** Is the friction driven by manual touchscreen typing fatigue, aggressive field-level validation errors (e.g., zip/postal code formatting), or lack of native browser autofill / location lookup integrations?

---

### PROB-02: Delivery Fee Sticker Shock on Sub-$75 Baskets
- **User Journey Stage:** Checkout — Shipping Review (`shipping_view` $\to$ `payment_select`).
- **Observed Problem:** Checkout abandonment escalates sharply when shipping fees impose a heavy proportional surcharge on low-ticket carts.
- **Empirical Evidence:** Shipping review abandonment rises from $6.16\%$ for free-shipping orders ($\ge \$75$) to $19.73\%$ for $\$40\text{--}\$60$ carts and $27.49\%$ for sub-$\$40$ carts. Logistic regression demonstrates that each $+10$ percentage point increase in `shipping_cost / cart_value` increases the odds of abandoning by $+49.3\%$ ($\text{OR} = 1.493, p < 10^{-100}$). Near-threshold carts ($\$60\text{--}\$74.99$) exhibit the highest backtracking rate ($9.29\%$) as users search for items to qualify for free shipping. Total shipping dropouts across all carts number $2,143$ sessions ($1,567$ in sub-$\$75$ carts).
- **Affected Segment:** Shoppers with basket values below the $\$75$ free-shipping threshold ($6,475$ checkout sessions reaching shipping).
- **Business Consequence:** $1,567$ abandoned checkout sessions among sub-threshold shoppers who had already completed address entry.
- **Confidence Level:** **High.**
- **Open Product Questions:** Would an interactive cart progress bar ("Add $\$12$ to unlock Free Shipping") or lower tiered shipping options reduce drop-off without eroding net margin?

---

### PROB-03: Unrecovered Payment Declines & Gateway Timeouts
- **User Journey Stage:** Checkout — Payment Authorization (`payment_attempt` $\to$ `payment_success` / `order_completed`).
- **Observed Problem:** Over $47\%$ of checkout sessions that encounter a payment failure permanently abandon without successfully completing an order.
- **Empirical Evidence:** $857$ checkout sessions encountered gateway declines ($6.52\%$ attempt decline rate). While $448$ sessions ($52.28\%$) recovered via retries or method switching, **$409$ checkout sessions permanently abandoned** without completing their purchase. Net Banking ($11.64\%$ failure) and Debit Cards ($8.72\%$ failure) suffered substantially higher decline rates than Digital Wallets ($3.41\%$). $25.9\%$ of failed users exited immediately after their first decline.
- **Affected Segment:** High-intent shoppers attempting payment ($857$ failed sessions).
- **Business Consequence:** Permanent loss of $409$ highly qualified prospective orders representing approximately $\$45,000+$ in unrealized GMV.
- **Confidence Level:** **High.**
- **Open Product Questions:** Do rigid, generic error messages discourage retries, and would smart instant fallbacks (e.g., auto-prompting 1-click Digital Wallets or instant retry) increase recovery rates?

---

### PROB-04: Pre-Checkout Promotional Code Rejection Attrition
- **User Journey Stage:** Shopping Cart — Promo Application (`add_to_cart` $\to$ `promo_applied` $\to$ `checkout_start`).
- **Observed Problem:** Shoppers who encounter promo code validation errors abandon the cart and exit prior to entering checkout at disproportionate rates.
- **Empirical Evidence:** Cart sessions triggering an invalid promo code error (`ERR_INVALID_PROMO`) advance to checkout at only **$41.25\%$** compared to **$62.57\%$** for non-promo carts (a $-21.32\text{ percentage point}$ deficit, $\chi^2 = 244.1, p < 10^{-50}$). Final session conversion drops to $26.56\%$ vs $40.32\%$.
- **Affected Segment:** Price-sensitive coupon hunters and promotional code users ($1,423$ cart sessions).
- **Business Consequence:** $836$ cart sessions lost pre-checkout due to promo code rejection.
- **Confidence Level:** **Moderate-High (Subject to Selection Bias).**
- **Open Product Questions:** Does prominent promo code input box placement encourage users to leave the site to hunt for coupons, and would collapsible fields or auto-applied valid coupons reduce attrition?

---

### PROB-05: First-Time Visitor Guest Checkout Onboarding Barrier
- **User Journey Stage:** Multi-Stage Checkout Funnel (`cart` $\to$ `address` $\to$ `shipping` $\to$ `purchase`).
- **Observed Problem:** First-time/new visitors convert at a $+48\%$ lower rate than returning customers ($9.08\%$ vs $13.46\%$), compounding across cart addition and address entry.
- **Empirical Evidence:** New visitors suffer a $20.21\%$ dropout at address entry compared to $12.51\%$ for returning customers. In a multivariate model, returning customers exhibit $+55.2\%$ higher adjusted odds of completing purchase ($\text{OR} = 1.5518, p < 10^{-100}$) after controlling for device and channel.
- **Affected Segment:** New visitor traffic ($62.18\%$ of total site sessions, $74,612$ sessions).
- **Business Consequence:** Massive monetization drag across the majority of incoming traffic.
- **Confidence Level:** **High (Observational Pattern).**
- **Open Product Questions:** Is the new customer gap caused by form-filling fatigue, lack of saved payment credentials, or trust hesitation on an unfamiliar marketplace?

---

### PROB-06: High-Ticket Cart Payment Friction & Limit Declines
- **User Journey Stage:** Checkout — Payment Selection & Authorization.
- **Observed Problem:** High-value baskets ($>\$300$) experience elevated payment-stage drop-off and card decline rates.
- **Empirical Evidence:** Carts exceeding $\$300$ exhibit a payment drop-off rate of $8.4\%$ compared to $4.8\%$ for baskets under $\$50$ ($\chi^2 = 23.29, p < 0.0001$). High-ticket credit card attempts suffer a $7.52\%$ decline rate (elevated by card limit and bank risk algorithm blocks) compared to $3.27\%$ for digital wallets.
- **Affected Segment:** High-GMV checkout sessions ($1,279$ payment dropouts; mean basket $\$111.96$, with top-tier $> \$300$).
- **Business Consequence:** Disproportionate loss of high-margin, top-revenue transactions.
- **Confidence Level:** **Moderate-High.**
- **Open Product Questions:** Would earlier prominence of Buy Now Pay Later (BNPL) installment options or multi-card split payment methods reduce payment declines for high-value orders?
