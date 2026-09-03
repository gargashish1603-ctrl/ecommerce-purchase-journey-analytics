# ShopSphere Experiment Catalog & A/B Testing Specifications

This catalog details the experimental designs, testable hypotheses, metric formulations, and governance criteria for the candidate Phase 5 experimentation portfolio.

---

## EXP-01: Mobile Address Autocomplete & Input Streamlining

- **Experiment ID:** `EXP-01`
- **Target Problem ID:** `PROB-01` (Mobile Address Form Friction)
- **Primary Objective:** `OBJ-01` (Reduce mobile address-entry latency and dropout)
- **Candidate Intervention:** Real-time address autocomplete dropdown API (`FR-ADDR-101`) combined with mobile numeric keypads and inline validation (`FR-ADDR-102`, `FR-ADDR-103`).
- **Control (A):** Existing multi-field manual address form without autocomplete suggestions.
- **Treatment (B):** Single-line street address search field with Google Places / Postal API autocomplete dropdown and automated City/State/ZIP population upon selection.

### Testable Hypothesis:
> *"If providing real-time address autocomplete reduces mobile touchscreen typing burden, then mobile checkout progression from address entry to shipping review will increase relative to control, without increasing downstream delivery address validation error rates."*

### Metric Architecture:
1. **Primary Metric:** **Mobile Address Stage Pass Rate (`passed_address_pct`)**
   - *Formula:* $\frac{\text{Count of Mobile Sessions reaching } \texttt{shipping\_view}}{\text{Count of Mobile Sessions reaching } \texttt{address\_entry}} \times 100\%$
   - *Baseline:* **$79.18\%$** ($10,483 / 13,239$ mobile address starters).
   - *Expected Direction:* **Positive** (Target planning assumption: $+4.0\%$ relative lift $\to 82.35\%$).
   - *Event Source:* `events.event_type IN ('address_entry', 'shipping_view') WHERE device_type = 'mobile'`.
2. **Secondary Metrics:**
   - *Mobile Address Dwell Time:* Median seconds between `address_entry` and `shipping_view` (Baseline: $45.0\text{s}$, target: $<38\text{s}$).
   - *Mobile Full-Funnel Conversion Rate:* Mobile session-to-purchase CVR (Baseline: $10.40\%$).
3. **Guardrail Metrics:**
   - *Address Validation Error Rate:* Percentage of address submissions returning format errors (Must not increase by $>0.10\text{ pp}$).
   - *API Latency Overhead:* Autocomplete response time ($p95 \le 200\text{ms}$).

### Experiment Operations & Governance:
- **Eligible Population:** All mobile web and smartphone sessions initiating checkout (`device_type == 'mobile' AND reached_checkout == True`).
- **Exclusion Criteria:** Desktop and tablet traffic; sessions with pre-saved returning customer addresses.
- **Randomization Unit:** Unique User Session (`session_id`), hashed 50/50 via deterministic MurmurHash3.
- **Sample Size per Arm:** $2,430$ mobile address sessions ($\alpha = 0.05, \text{Power} = 0.80, \text{MDE} = +4.0\%$).
- **Total Sample Required:** $4,860$ mobile address sessions.
- **Estimated Duration:** **33 days (~5 weeks)** based on $147.1$ daily mobile address sessions.
- **Decision Rule:**
  - **SHIP:** Statistically significant increase in Primary Metric ($p < 0.05$, relative lift $\ge +2.5\%$) with no violation of Address Validation Error guardrail.
  - **ITERATE:** Lift positive ($+1.0\%\text{--}+2.4\%$) but statistically inconclusive; refine dropdown search debouncing and test for additional 2 weeks.
  - **ROLLBACK:** Negative conversion impact ($p < 0.05$) or Address Validation Error rate increases by $>0.20\text{ pp}$.

---

## EXP-02: Dynamic Free Shipping Progress Bar & Add-On Recommendations

- **Experiment ID:** `EXP-02`
- **Target Problem ID:** `PROB-02` (Sub-$75 Shipping Fee Sticker Shock)
- **Primary Objective:** `OBJ-02` (Increase threshold awareness and reduce shipping review drop-off)
- **Candidate Intervention:** Interactive Free Shipping progress bar on cart drawer and cart summary (`FR-SHIP-201`) with 1-click threshold add-on recommendations (`FR-SHIP-202`).
- **Control (A):** Static cart summary showing subtotal and calculating shipping fee only at step 2 of checkout.
- **Treatment (B):** Visual progress bar displaying remaining dollar amount needed to unlock free shipping with dynamic 1-click low-cost add-on recommendations for carts between $\$50.00$ and $\$74.99$.

### Testable Hypothesis:
> *"If making the $75 free shipping threshold prominently visible in the cart alongside relevant low-cost add-ons reduces surprise shipping costs, then sub-$75 cart-to-purchase conversion will increase and sub-$75 basket sizes will expand relative to control without reducing net shipping margin contribution."*

### Metric Architecture:
1. **Primary Metric:** **Sub-$\$75$ Cart-to-Purchase Conversion Rate (`sub75_cart_to_purchase_cvr`)**
   - *Formula:* $\frac{\text{Count of Sub-}{\$75}\text{ Cart Sessions Completing Purchase}}{\text{Count of Total Sub-}{\$75}\text{ Cart Sessions}} \times 100\%$
   - *Baseline:* **$34.36\%$** ($4,455 / 12,967$ sessions).
   - *Expected Direction:* **Positive** (Target planning assumption: $+7.5\%$ relative lift $\to 36.93\%$).
   - *Event Source:* `sessions.parquet` where initial cart value $<\$75.00$.
2. **Secondary Metrics:**
   - *Sub-$\$75$ Average Order Value (AOV):* Mean final cart value for initially sub-$\$75$ carts (Baseline: $\$38.80$).
   - *Shipping Review Stage Abandonment Rate:* Percentage of shipping view sessions abandoning at shipping (Baseline: $24.20\%$).
   - *Threshold Crossing Rate:* Percentage of initially sub-$\$75$ carts that reach $\ge \$75$ before checkout (Baseline: $4.2\%$).
3. **Guardrail Metrics:**
   - *Net Shipping Contribution Margin:* Gross shipping fee revenue minus actual delivery cost per order (Must not drop by $>2.0\%$).
   - *Cart Abandonment Rate on $\ge \$75$ Carts:* Must remain neutral ($\pm 0.5\text{ pp}$).

### Experiment Operations & Governance:
- **Eligible Population:** All sessions forming a shopping cart with initial value $<\$75.00$.
- **Exclusion Criteria:** Sessions with initial cart value $\ge \$75.00$.
- **Randomization Unit:** User Session (`session_id`), 50/50 split.
- **Sample Size per Arm:** $5,423$ sessions ($\alpha = 0.05, \text{Power} = 0.80, \text{MDE} = +7.5\%$).
- **Total Sample Required:** $10,846$ sub-$\$75$ cart sessions.
- **Estimated Duration:** **75 days (~11 weeks)** based on $144.1$ daily sub-$\$75$ cart sessions.
- **Decision Rule:**
  - **SHIP:** Primary Metric achieves statistically significant lift ($p < 0.05$, lift $\ge +5.0\%$) and Net Margin Contribution remains positive or neutral.
  - **ITERATE:** AOV increases significantly ($+\$3.00+$) but conversion lift is neutral; optimize add-on product selection algorithms.
  - **ROLLBACK:** Significant drop in net margin contribution ($>3.0\%$) or conversion decreases.

---

## EXP-03: Smart Payment Decline Recovery & Instant Alternative APM Prompt

- **Experiment ID:** `EXP-03`
- **Target Problem ID:** `PROB-03` (Unrecovered Payment Declines)
- **Primary Objective:** `OBJ-03` (Recover qualified checkout sessions encountering gateway failures)
- **Candidate Intervention:** Contextual soft-decline recovery modal with 1-click fallback to Digital Wallets (`FR-PAY-301`, `FR-PAY-302`).
- **Control (A):** Standard inline red error message banner ("Payment authorization failed. Please try again or use another card").
- **Treatment (B):** Focused Smart Recovery Modal explaining the soft decline in clear language with pre-configured 1-click Apple Pay / Google Pay / PayPal buttons and retry state retention.

### Testable Hypothesis:
> *"If presenting customers who experience soft payment declines with clear recovery guidance and instant 1-click alternative payment methods reduces exit hesitation, then payment failure recovery rates will increase relative to control, recovering lost orders."*

### Metric Architecture:
1. **Primary Metric:** **Payment Failure-to-Success Recovery Rate (`payment_recovery_rate_pct`)**
   - *Formula:* $\frac{\text{Count of Failed Payment Sessions Successfully Completing Order}}{\text{Count of Total Sessions Encountering Payment Decline}} \times 100\%$
   - *Baseline:* **$52.28\%$** ($448 / 857$ sessions).
   - *Expected Direction:* **Positive** (Target planning assumption: $+15.0\%$ relative lift $\to 60.12\%$).
   - *Event Source:* `events.parquet` where session contains $\ge 1$ `payment_failed` event.
2. **Secondary Metrics:**
   - *Alternative Payment Method Switch Rate:* Percentage of failed sessions that attempt a different payment method (Baseline: $17.50\%$).
   - *Immediate Exit Rate Post-Decline:* Percentage of failed sessions exiting within 30 seconds with 0 retries (Baseline: $25.90\%$).
3. **Guardrail Metrics:**
   - *Fraud / Risk Block Rate:* Fraud dispute and chargeback rate on recovered transactions (Must not exceed platform threshold of $0.5\%$).
   - *Double-Charge Incident Rate:* Zero tolerance ($0.00\%$) for duplicate charge authorization events.

### Experiment Operations & Governance:
- **Eligible Population:** All checkout sessions encountering a soft payment gateway decline (`ERR_GATEWAY_TIMEOUT`, `ERR_3DS_AUTH_FAILED`, `ERR_INSUFFICIENT_FUNDS`, `ERR_BANK_DECLINE`).
- **Exclusion Criteria:** Hard fraud block decline codes (`ERR_FRAUD_BLOCK`, `ERR_CARD_STOLEN`).
- **Randomization Unit:** Checkout Session (`session_id`), assigned 50/50 upon first payment attempt.
- **Sample Size per Arm:** $628$ failed payment sessions ($\alpha = 0.05, \text{Power} = 0.80, \text{MDE} = +15.0\%$).
- **Total Sample Required:** $1,256$ failed payment sessions.
- **Estimated Duration:** **132 days (~19 weeks)** based on $9.5$ daily payment decline sessions. *(Note: Can be accelerated by expanding traffic or prioritizing high-volume debit/net-banking segments).*
- **Decision Rule:**
  - **SHIP:** Statistically significant increase in Recovery Rate ($p < 0.05$, lift $\ge +10.0\%$) with zero duplicate charges.
  - **ITERATE:** Recovery rate lift is positive but below significance threshold; refine modal copy and APM button hierarchy.
  - **ROLLBACK:** Any occurrence of technical double-charging or decline in customer trust.

---

## EXP-04: Collapsible Promo Code Drawer & Inline Deal Transparency

- **Experiment ID:** `EXP-04`
- **Target Problem ID:** `PROB-04` (Promo Code Rejection Attrition)
- **Primary Objective:** `OBJ-04` (Reduce pre-checkout cart abandonment from coupon hunting and errors)
- **Candidate Intervention:** Collapsible promo code link (`FR-PROMO-401`), friendly inline error messaging (`FR-PROMO-402`), and eligible store deals carousel (`FR-PROMO-403`).
- **Control (A):** Prominently exposed, empty promo code text box in the cart drawer with standard red error messages upon invalid submission.
- **Treatment (B):** Collapsed text link (*"+ Have a promo code?"*) that expands upon tap, paired with a display of active verified store promotions and friendly error feedback.

### Testable Hypothesis:
> *"If de-emphasizing the empty promo code input box reduces off-site coupon hunting while displaying verified store deals reduces rejection disappointment, then cart-to-checkout initiation will increase relative to control without inflating overall discount expenditure."*

### Metric Architecture:
1. **Primary Metric:** **Cart-to-Checkout Initiation Rate (`cart_to_checkout_rate_pct`)**
   - *Formula:* $\frac{\text{Count of Cart Sessions reaching } \texttt{checkout\_start}}{\text{Count of Total Sessions reaching } \texttt{add\_to\_cart}} \times 100\%$
   - *Baseline:* **$61.60\%$** ($19,931 / 32,354$ cart sessions).
   - *Expected Direction:* **Positive** (Target planning assumption: $+3.0\%$ relative lift $\to 63.45\%$).
   - *Event Source:* `sessions.parquet` (`reached_checkout / reached_cart`).
2. **Secondary Metrics:**
   - *Invalid Promo Error Frequency:* Number of `ERR_INVALID_PROMO` events per 1,000 cart sessions (Baseline: $44.0$).
   - *Cart Dwell Time Pre-Checkout:* Dwell time in cart prior to checkout initiation.
3. **Guardrail Metrics:**
   - *Gross Discount Expenditure Rate:* Total promotional discount dollars divided by Total GMV (Must not increase by $>0.50\text{ pp}$).
   - *Cart-to-Purchase Conversion:* Must not decrease.

### Experiment Operations & Governance:
- **Eligible Population:** All sessions adding $\ge 1$ item to cart (`reached_cart == True`).
- **Exclusion Criteria:** None.
- **Randomization Unit:** User Session (`session_id`), 50/50 split.
- **Sample Size per Arm:** $10,768$ cart sessions ($\alpha = 0.05, \text{Power} = 0.80, \text{MDE} = +3.0\%$).
- **Total Sample Required:** $21,536$ cart sessions.
- **Estimated Duration:** **60 days (~9 weeks)** based on $359.5$ daily cart sessions.
- **Decision Rule:**
  - **SHIP:** Statistically significant increase in Cart-to-Checkout Rate ($p < 0.05$, lift $\ge +2.0\%$) with Gross Discount Expenditure within budget.
  - **ITERATE:** Cart progression increases but discount rate exceeds threshold; tighten promo eligibility rules.
  - **ROLLBACK:** Cart-to-checkout rate declines or promo abuse detected.
