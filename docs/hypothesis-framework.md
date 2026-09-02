# Hypothesis Framework

> **Important Note:** The hypotheses listed below represent structured testable propositions formulated prior to data analysis. They do **not** represent verified findings or predetermined conclusions. Each hypothesis will be empirically evaluated during the SQL and Python analytical phases.

---

### Summary of Hypotheses

| Hypothesis ID | Category | Core Proposition |
| :--- | :--- | :--- |
| **H1** | Device / UX | Mobile users experience higher drop-off rates at form-intensive checkout stages (Address Entry) than Desktop users. |
| **H2** | Checkout Friction | Elevated dwell time during checkout steps is positively associated with session abandonment. |
| **H3** | Payment Dynamics | Initial payment failures do not automatically cause abandonment; recovery is moderated by retry attempts and payment method switching. |
| **H4** | Customer Maturity | Returning customers exhibit higher checkout conversion and lower drop-off at payment stages compared to first-time visitors. |
| **H5** | Commercial Policy | A higher shipping-cost-to-cart-value ratio (`shipping_ratio`) is positively associated with abandonment at the shipping review stage. |
| **H6** | Acquisition Channel | Traffic acquisition channels with direct/transactional intent (Search, Direct, CRM) convert at higher rates than discovery channels (Paid Social). |
| **H7** | Browsing Behavior | Excessive product browsing prior to cart addition reflects decision hesitation and correlates with lower checkout completion rates. |
| **H8** | Cart Value Tier | High-value carts experience greater abandonment at the payment method selection stage due to payment threshold friction or credit limits. |
| **H9** | Promotional Friction | Applying an invalid or rejected discount code at checkout increases immediate session abandonment. |
| **H10** | Path Backtracking | Sessions exhibiting backtracking behavior (navigating from checkout back to cart/catalog) have significantly lower conversion probabilities. |

---

## Detailed Hypothesis Specifications

### H1: Mobile Checkout Form Friction
- **Hypothesis ID:** `H1`
- **Hypothesis:** Mobile users experience a disproportionately higher drop-off rate at the Address Entry stage compared to desktop users due to mobile input friction and form length.
- **Why It Is Plausible:** Typing full postal addresses, names, and contact details on mobile keyboards involves higher physical interaction effort, higher error rates, and increased cognitive fatigue compared to desktop keyboards.
- **Data Required:** `events` table filtered for `checkout_start` and `address_entry_success`/`address_entry_abandoned`, segmented by `device_type`.
- **Metric(s):** Address Stage Completion Rate (`sessions completing address / sessions starting address`), Mobile vs. Desktop relative completion ratio.
- **Potential Confounders:** Customer type (new users fill forms; returning users may have pre-filled addresses), network connection speed, user age demographics.
- **Analysis Method:** Chi-square test of independence for step progression across devices; logistic regression controlling for `customer_type` and `cart_value`.
- **Supporting Evidence:** Statistically significant lower completion rate at Address Entry on mobile after controlling for customer type.
- **Weakening/Rejecting Evidence:** Mobile address completion rate is comparable to or higher than desktop, or drop-off is evenly distributed across all checkout steps rather than concentrated at form input.

---

### H2: Checkout Dwell Time & Hesitation Friction
- **Hypothesis ID:** `H2`
- **Hypothesis:** Sessions with checkout step dwell times exceeding the median by more than 1.5× Interquartile Ranges (IQR) have a higher likelihood of abandoning the funnel.
- **Why It Is Plausible:** Prolonged duration at a single checkout step often signals confusion, form validation errors, price recalculation hesitation, or seeking alternative off-site options.
- **Data Required:** Step-level dwell times (`time_since_previous_event` between consecutive checkout milestones), session conversion outcome.
- **Metric(s):** Median/IQR step dwell time (seconds), Abandonment rate by dwell time quartile/decile.
- **Potential Confounders:** Device type, cart item count, payment method complexity (e.g., 3D-Secure SMS wait times).
- **Analysis Method:** Non-parametric Mann-Whitney U test comparing dwell times of converted vs. abandoned sessions; survival/duration curves.
- **Supporting Evidence:** Significantly longer dwell times in abandoned sessions; sharp uptick in abandonment probability in high-dwell deciles.
- **Weakening/Rejecting Evidence:** Abandoned sessions show near-instant drop-offs (<5 seconds) or identical dwell time distributions to completed sessions.

---

### H3: Payment Failure Recovery Dynamics
- **Hypothesis ID:** `H3`
- **Hypothesis:** A substantial portion of customers encountering an initial payment failure can be recovered if they attempt retries or switch payment methods.
- **Why It Is Plausible:** Customers reaching the payment execution stage have demonstrated strong purchase intent; technical declines or typos can be resolved if the UI facilitates immediate retries or alternative payment options.
- **Data Required:** Event logs tracking `payment_attempt`, `payment_failed`, `payment_retried`, `payment_method_switched`, and `order_completed`.
- **Metric(s):** Payment Failure Rate, Retry Rate (`retries / failures`), Method Switch Rate, Eventual Recovery Conversion Rate (`recovered purchases / initial failures`).
- **Potential Confounders:** Error type (transient gateway timeout vs. hard card decline/insufficient funds), cart value.
- **Analysis Method:** Transition matrix analysis, sequential event path tracing, and logistic regression on recovery drivers.
- **Supporting Evidence:** Sessions with retries or payment method switches achieve meaningful recovery conversion rates (>20-30%).
- **Weakening/Rejecting Evidence:** Payment failure leads almost deterministically (>95%) to instant session termination regardless of retry prompts or payment options.

---

### H4: New vs. Returning Customer Maturity Dynamics
- **Hypothesis ID:** `H4`
- **Hypothesis:** Returning customers have a significantly higher progression rate through the checkout funnel and lower sensitivity to shipping fees than first-time visitors.
- **Why It Is Plausible:** Returning customers have established platform trust, are familiar with the fulfillment experience, and likely possess saved checkout preferences.
- **Data Required:** Funnel event sequences segmented by `customer_type` (`new` vs. `returning`), order values, shipping costs.
- **Metric(s):** Full-funnel conversion rate, Stage-by-stage progression rate, Checkout completion rate by customer type.
- **Potential Confounders:** Acquisition channel mix (returning users come via Direct/CRM; new users via Paid Ads).
- **Analysis Method:** Two-proportion Z-tests, stratified funnel conversion breakdown by channel and customer type.
- **Supporting Evidence:** Returning customers exhibit higher progression rates across every checkout step, particularly at Address and Payment.
- **Weakening/Rejecting Evidence:** New and returning users show statistically indistinguishable step-level drop-off rates across checkout stages.

---

### H5: Shipping Cost to Cart Value Ratio (Sticker Shock)
- **Hypothesis ID:** `H5`
- **Hypothesis:** A higher ratio of shipping cost to cart value (`shipping_cost / cart_value`) increases abandonment at the Shipping View stage.
- **Why It Is Plausible:** When shipping fees represent a high percentage of the order (e.g., >15-20%), customers perceive low value and experience "fee shock," triggering abandonment.
- **Data Required:** `cart_value`, `shipping_cost`, `shipping_ratio`, and drop-off indicators at the `shipping_view` stage.
- **Metric(s):** Abandonment rate at Shipping View across `shipping_ratio` bins (e.g., 0% Free, <5%, 5-10%, 10-20%, >20%).
- **Potential Confounders:** Product category (bulky items naturally incur higher fees), overall cart value.
- **Analysis Method:** Logistic regression predicting shipping stage drop-off as a function of `shipping_ratio`, controlling for category and cart size; binned conversion response curves.
- **Supporting Evidence:** Monotonic increase in drop-off rate as shipping ratio increases, with a noticeable threshold cliff.
- **Weakening/Rejecting Evidence:** Shipping stage drop-off is uncorrelated with shipping fee proportion or remains constant across fee tiers.

---

### H6: Acquisition Channel Intent Disparities
- **Hypothesis ID:** `H6`
- **Hypothesis:** High-intent acquisition channels (Direct, Organic Search, CRM) yield higher cart-to-purchase conversion than discovery channels (Paid Social, Display).
- **Why It Is Plausible:** Users actively searching for a product or responding to tailored CRM emails possess pre-formed transactional intent, whereas social media visitors browse casually.
- **Data Required:** `acquisition_channel`, macro funnel milestone reach rates, order completion.
- **Metric(s):** Visitor-to-Cart Rate, Cart-to-Checkout Rate, Checkout-to-Purchase Rate by channel.
- **Potential Confounders:** Device mix across channels (Paid Social is predominantly mobile), promotional campaign targeting.
- **Analysis Method:** Multi-channel funnel comparison, ANOVA / Kruskal-Wallis tests across channel groups.
- **Supporting Evidence:** Conversion rates from Cart to Purchase are systematically higher for Search/Direct/CRM than Paid Social after adjusting for device.
- **Weakening/Rejecting Evidence:** Channel conversion rates are uniform once users reach the cart stage.

---

### H7: Browsing Depth vs. Purchase Intent
- **Hypothesis ID:** `H7`
- **Hypothesis:** Excessive product page views (>80th percentile) prior to cart addition correlate with lower checkout completion rates compared to focused browsing.
- **Why It Is Plausible:** Extensive multi-product browsing without committing to cart often reflects window shopping, decision paralysis, or comparison shopping without immediate intent to buy.
- **Data Required:** Count of `product_view` events prior to the first `add_to_cart` event per session, eventual purchase status.
- **Metric(s):** Pre-cart browsing count, Cart-to-purchase conversion rate across browsing depth quartiles.
- **Potential Confounders:** Product category complexity (Electronics vs. Beauty), session duration.
- **Analysis Method:** Correlation analysis, segmented conversion probability curves across browsing depth bins.
- **Supporting Evidence:** An inverted-U or decaying relationship where moderate browsing converts best, while extreme browsing shows depressed conversion.
- **Weakening/Rejecting Evidence:** Conversion rate increases strictly monotonically with product browsing depth.

---

### H8: High-Value Cart Checkout Friction
- **Hypothesis ID:** `H8`
- **Hypothesis:** High-value carts experience higher abandonment at the payment stage than moderate-value carts, driven by card spending limit friction or lack of BNPL / financing options.
- **Why It Is Plausible:** Transactions with high price tags trigger stricter bank fraud checks, OTP verifications, card limit declines, and greater buyer remorse at the final payment confirmation step.
- **Data Required:** `cart_value` tiers, payment method chosen, payment success/failure rates, final completion.
- **Metric(s):** Payment Stage Drop-off Rate by Cart Value Tier (<$50, $50-$150, $150-$300, >$300), Payment decline rate by cart tier.
- **Potential Confounders:** Customer type, product category mix (Electronics vs. Fashion).
- **Analysis Method:** Logistic regression on payment completion with cart value interactions; payment decline frequency by price tier.
- **Supporting Evidence:** Significantly higher payment failure and drop-off rates for top quartile cart values, especially on standard credit cards.
- **Weakening/Rejecting Evidence:** High-value carts complete payment at equal or higher rates than lower-value carts.

---

### H9: Promo Code Rejection & Checkout Abandonment
- **Hypothesis ID:** `H9`
- **Hypothesis:** Sessions that trigger a promo code failure or invalid code event have a higher likelihood of abandoning checkout than sessions with valid or no promo codes.
- **Why It Is Plausible:** An invalid discount attempt leaves users feeling they are overpaying or missing out on a deal, prompting them to leave to search for valid coupons or abandon entirely.
- **Data Required:** Discount application events (`promo_applied_success`, `promo_applied_failure`), subsequent checkout step completion.
- **Metric(s):** Abandonment rate following promo failure vs. baseline checkout abandonment.
- **Potential Confounders:** Cart value, customer sensitivity.
- **Analysis Method:** Cohort comparison, relative risk of abandonment post-promo failure.
- **Supporting Evidence:** Immediate spike in session exit rates following an invalid discount code attempt.
- **Weakening/Rejecting Evidence:** Users encountering promo code errors continue through the checkout funnel at the same rate as others.

---

### H10: Backtracking & Cyclical Navigation Friction
- **Hypothesis ID:** `H10`
- **Hypothesis:** Sessions containing backward event sequences (e.g., `checkout_start` → `cart_view` or `product_view`) have a lower purchase completion rate than linear progression sessions.
- **Why It Is Plausible:** Backtracking indicates item second-guessing, unexpected shipping costs, or missing product details that force the user out of the transactional flow.
- **Data Required:** Event order sequence analysis, state transition count from checkout back to browsing/cart.
- **Metric(s):** Backtracking Session Share, Conversion Rate of Backtracking vs. Linear Sessions.
- **Potential Confounders:** Cart modification (adding more items to meet free shipping threshold).
- **Analysis Method:** Sequence mining, transition matrix graph analysis, Fisher's exact test.
- **Supporting Evidence:** Lower overall conversion for backtracking sessions, except in sub-cohorts that add items to qualify for free shipping.
- **Weakening/Rejecting Evidence:** Backtracking sessions convert at equal or higher rates across all scenarios.
