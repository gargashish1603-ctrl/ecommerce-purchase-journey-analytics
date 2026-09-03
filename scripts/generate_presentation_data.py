"""
ShopSphere Presentation Data Generator
======================================
Compiles all audited canonical metrics from Phases 1-5 into a structured,
type-safe presentation dataset for the portfolio web application.
"""

import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "presentation", "src", "data", "case-study-data.json")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

data = {
    "disclaimer": "ShopSphere is a fictional e-commerce marketplace case study. The dataset is synthetic and was generated to simulate realistic purchase-journey behavior. Findings demonstrate analytical and product methodology rather than real company performance.",
    "methodology_tagline": "Observe → Investigate → Diagnose → Define → Experiment",
    "headline_metrics": [
        {"label": "Total Sessions", "value": "120,000", "description": "Distinct customer browsing journeys across 90 simulated days", "highlight": False},
        {"label": "Clickstream Events", "value": "689,508", "description": "Granular session events tracked across the full customer funnel", "highlight": False},
        {"label": "Completed Purchases", "value": "12,888", "description": "Successfully fulfilled orders with completed payment capture", "highlight": False},
        {"label": "Purchase Conversion", "value": "10.74%", "description": "Session-level conversion rate across entire marketplace traffic", "highlight": True},
        {"label": "Hypotheses Evaluated", "value": "10", "description": "Formal research questions tested with rigorous statistical controls", "highlight": False}
    ],
    "journey_stages": [
        {
            "id": 1,
            "name": "Session Start",
            "event": "session_start",
            "sessions_reached": 120000,
            "traffic_share": "100.0%",
            "dropoff_sessions": 0,
            "pass_rate": "100.0%",
            "description": "Visitor arrives on ShopSphere from organic, paid, direct, or referral acquisition channels.",
            "key_finding": "Mobile accounts for 66.7% (80,016 sessions) of initial inbound traffic.",
            "doc_ref": "analysis/01_data_profile.md"
        },
        {
            "id": 2,
            "name": "Product View",
            "event": "product_view",
            "sessions_reached": 120000,
            "traffic_share": "100.0%",
            "dropoff_sessions": 87646,
            "pass_rate": "26.96%",
            "description": "Customer explores catalog product detail pages, reviews specifications, pricing, and ratings.",
            "key_finding": "87,646 sessions (73.0%) terminate during browsing without adding items to cart (Discovery Bouncers).",
            "doc_ref": "analysis/root_cause_browsing.md"
        },
        {
            "id": 3,
            "name": "Add to Cart",
            "event": "add_to_cart",
            "sessions_reached": 32354,
            "traffic_share": "26.96%",
            "dropoff_sessions": 0,
            "pass_rate": "100.0%",
            "description": "Customer demonstrates high commercial intent by placing one or more items into their shopping cart.",
            "key_finding": "Cart addition rate is 30.90% for 1-page viewers but falls to 9.20% for 7+ page viewers.",
            "doc_ref": "analysis/02_funnel_analysis.md"
        },
        {
            "id": 4,
            "name": "Cart View & Review",
            "event": "cart_view",
            "sessions_reached": 32354,
            "traffic_share": "26.96%",
            "dropoff_sessions": 12423,
            "pass_rate": "61.60%",
            "description": "Customer opens the cart drawer or cart page, reviews subtotal, and tests promotional coupon codes.",
            "key_finding": "12,423 sessions abandon at cart. Invalid promo code errors reduce checkout progression by -21.3pp.",
            "doc_ref": "analysis/root_cause_promo.md"
        },
        {
            "id": 5,
            "name": "Checkout Start",
            "event": "checkout_start",
            "sessions_reached": 19931,
            "traffic_share": "16.61%",
            "dropoff_sessions": 0,
            "pass_rate": "100.0%",
            "description": "Customer initiates active checkout funnel, transitioning from shopping cart to order execution.",
            "key_finding": "19,931 checkout starters represent the high-intent golden cohort where 7,043 total drops occur.",
            "doc_ref": "analysis/terminal_state_diagnosis.md"
        },
        {
            "id": 6,
            "name": "Address Entry",
            "event": "address_entry",
            "sessions_reached": 19931,
            "traffic_share": "16.61%",
            "dropoff_sessions": 3621,
            "pass_rate": "81.83%",
            "description": "Customer enters shipping destination, contact details, and recipient postal information.",
            "key_finding": "Mobile pass rate is 79.18% vs Desktop 87.07% (Adj OR = 0.5704), driving 1,043.7 mobile excess lost sessions.",
            "doc_ref": "analysis/root_cause_address.md"
        },
        {
            "id": 7,
            "name": "Shipping Review",
            "event": "shipping_view",
            "sessions_reached": 16310,
            "traffic_share": "13.59%",
            "dropoff_sessions": 2143,
            "pass_rate": "87.85%",
            "description": "Customer reviews shipping carrier options, delivery time estimates, and delivery fee surcharges.",
            "key_finding": "Sub-$75 carts suffer 24.20% drop-off (1,567 dropouts) due to shipping fee ratio sticker shock.",
            "doc_ref": "analysis/root_cause_shipping.md"
        },
        {
            "id": 8,
            "name": "Payment Selection",
            "event": "payment_select",
            "sessions_reached": 14328,
            "traffic_share": "11.94%",
            "dropoff_sessions": 1279,
            "pass_rate": "89.95%",
            "description": "Customer chooses payment instrument (Credit Card, Debit Card, Digital Wallet, Net Banking).",
            "key_finding": "Baskets >$300 exhibit higher payment hesitation (8.4% drop-off) and elevated credit card limit declines.",
            "doc_ref": "analysis/05_payment_analysis.md"
        },
        {
            "id": 9,
            "name": "Payment Attempt",
            "event": "payment_attempt",
            "sessions_reached": 13148,
            "traffic_share": "10.96%",
            "dropoff_sessions": 857,
            "pass_rate": "93.48%",
            "description": "Payment authorization request is submitted to acquiring gateway and issuing bank network.",
            "key_finding": "857 sessions encounter payment declines (6.52% decline rate), concentrated in Net Banking (11.64%).",
            "doc_ref": "analysis/root_cause_payment.md"
        },
        {
            "id": 10,
            "name": "Payment Success / Recovery",
            "event": "payment_success",
            "sessions_reached": 12888,
            "traffic_share": "10.74%",
            "dropoff_sessions": 409,
            "pass_rate": "96.90%",
            "description": "Successful payment capture authorization confirmed by bank; unrecovered failures exit funnel.",
            "key_finding": "52.28% of failed sessions recover via retry/switch; 409 unrecovered checkout sessions permanently lost.",
            "doc_ref": "analysis/root_cause_payment.md"
        },
        {
            "id": 11,
            "name": "Order Completed",
            "event": "order_completed",
            "sessions_reached": 12888,
            "traffic_share": "10.74%",
            "dropoff_sessions": 0,
            "pass_rate": "100.0%",
            "description": "Order receipt generated, inventory allocated, and post-purchase confirmation rendered.",
            "key_finding": "Total fulfilled GMV captured: $1,405,948.40 across 12,888 orders (Average Order Value: $109.09).",
            "doc_ref": "analysis/01_data_profile.md"
        }
    ],
    "funnel_summary": {
        "macro_funnel": [
            {"step": "Total Sessions", "count": 120000, "conversion_from_top": "100.0%", "step_dropoff": 87646, "step_loss_pct": "73.04%", "description": "Marketplace traffic"},
            {"step": "Cart Addition", "count": 32354, "conversion_from_top": "26.96%", "step_dropoff": 12423, "step_loss_pct": "38.40%", "description": "Added >= 1 product"},
            {"step": "Checkout Started", "count": 19931, "conversion_from_top": "16.61%", "step_dropoff": 7043, "step_loss_pct": "35.34%", "description": "Active checkout funnel"},
            {"step": "Purchased", "count": 12888, "conversion_from_top": "10.74%", "step_dropoff": 0, "step_loss_pct": "0.0%", "description": "Completed orders"}
        ],
        "headline_insight": "Most sessions never reach checkout (73.0% drop pre-cart), but the highest-value product opportunities emerge deeper in the journey where high-intent buyers encounter fixable interface friction."
    },
    "prioritized_problems": [
        {
            "id": "PROB-01",
            "rank": 1,
            "title": "Mobile Address Form Input Friction",
            "stage": "Checkout — Address Entry",
            "priority": "P0 — Critical",
            "score": "8.85 / 10",
            "evidence_summary": "Mobile address pass rate is 79.18% vs Desktop 87.07% (Adj OR = 0.5704, p < 10^-36). Dwell time is +21.6% longer (45s vs 37s). Mobile accounts for 1,043.7 excess lost sessions relative to desktop baseline.",
            "affected_volume": "13,239 mobile checkout starters (1,043.7 excess losses)",
            "candidate_intervention": "Real-time address autocomplete API, native mobile numeric keypads, and 1-click Express Checkout.",
            "confidence": "High (Multivariate regression controlled for channel and customer maturity)",
            "experiment_id": "EXP-01"
        },
        {
            "id": "PROB-02",
            "rank": 2,
            "title": "Sub-$75 Shipping Fee Sticker Shock",
            "stage": "Checkout — Shipping Review",
            "priority": "P0 — Critical",
            "score": "8.85 / 10",
            "evidence_summary": "Shipping review abandonment jumps to 24.20% for sub-$75 carts (up to 27.49% for <$40 carts) vs 6.16% for free shipping orders (OR_10% = 1.4927). Backtracking peaks at 9.29% for $60-$74.99 carts.",
            "affected_volume": "6,475 sub-$75 shipping view sessions (1,567 lost checkouts)",
            "candidate_intervention": "Dynamic cart free shipping progress bar with 1-click low-cost catalog add-on recommendations.",
            "confidence": "High (Statistically significant fee elasticity across price bins)",
            "experiment_id": "EXP-02"
        },
        {
            "id": "PROB-03",
            "rank": 3,
            "title": "Unrecovered Payment Declines & Gateway Timeouts",
            "stage": "Checkout — Payment Authorization",
            "priority": "P0 — Critical",
            "score": "8.65 / 10",
            "evidence_summary": "857 payment declines occur (6.52% attempt decline rate). 47.72% of failed sessions permanently abandon without recovery, resulting in 409 lost prospective orders. 25.9% exit immediately post-decline.",
            "affected_volume": "857 failed payment sessions (409 permanently lost)",
            "candidate_intervention": "Smart soft-decline recovery modal with 1-click fallback to Digital Wallets (Apple Pay/Google Pay) and automated retry.",
            "confidence": "High (Observed event-level payment state transitions)",
            "experiment_id": "EXP-03"
        },
        {
            "id": "PROB-04",
            "rank": 4,
            "title": "Promo Code Rejection Attrition",
            "stage": "Shopping Cart — Promo Input",
            "priority": "P1 — High",
            "score": "7.55 / 10",
            "evidence_summary": "Cart sessions triggering invalid promo errors advance to checkout at only 41.25% vs 62.57% for non-promo carts (-21.32pp drop, p < 10^-50), associated with 836 pre-checkout cart abandonments.",
            "affected_volume": "1,423 invalid promo cart sessions (836 lost checkouts)",
            "candidate_intervention": "Collapsible promo drawer with asynchronous inline validation and active store promotions carousel.",
            "confidence": "Moderate-High (Observational association subject to coupon-hunter selection bias)",
            "experiment_id": "EXP-04"
        },
        {
            "id": "PROB-05",
            "rank": 5,
            "title": "First-Time Guest Checkout Barrier",
            "stage": "Multi-Stage Checkout Funnel",
            "priority": "P1 — High",
            "score": "7.45 / 10",
            "evidence_summary": "New visitors convert at 9.08% vs 13.46% for returning buyers (Adj OR = 1.5518 for returning, p < 10^-100). New visitors suffer a 20.21% dropout at address entry compared to 12.51% for returning buyers.",
            "affected_volume": "74,612 new visitor sessions (62.2% of total traffic)",
            "candidate_intervention": "Zero-password frictionless guest checkout with 1-click post-purchase account creation on receipt.",
            "confidence": "High (Multi-stage cohort progression gap confirmed across devices)",
            "experiment_id": "EXP-05 (Future)"
        },
        {
            "id": "PROB-06",
            "rank": 6,
            "title": "High-Ticket Cart Payment Friction & Limit Declines",
            "stage": "Checkout — Payment Selection",
            "priority": "P2 — Medium",
            "score": "7.10 / 10",
            "evidence_summary": "Orders >$300 experience higher payment stage drop-off (8.4% vs 4.8%) and elevated credit card decline rates (7.52%) due to bank authorization limits and risk challenge friction.",
            "affected_volume": "1,279 payment dropouts (top-tier carts >$300)",
            "candidate_intervention": "Prominent BNPL installment display (e.g., '4 payments of $75') and split-card payment options.",
            "confidence": "Moderate-High (Significant payment drop disparity on high baskets)",
            "experiment_id": "EXP-06 (Future)"
        }
    ],
    "evidence_board": {
        "mobile_address": {
            "title": "Mobile Address Form Entry Friction",
            "primary_metric": "79.18% Mobile Address Pass Rate",
            "comparison_metric": "87.07% Desktop Address Pass Rate",
            "gap": "-7.89 pp deficit",
            "adj_or": "0.5704",
            "ci_95": "0.5232 – 0.6220",
            "p_value": "4.48e-37",
            "dwell_time": "45.0s Mobile vs 37.0s Desktop (+21.6%)",
            "excess_loss": "1,043.7 excess lost sessions",
            "interpretation": "Mobile shoppers experience statistically significant higher address drop-off. The 1,043.7 excess loss represents estimated lost sessions above the desktop baseline rate, reflecting touchscreen input burden."
        },
        "shipping": {
            "title": "Sub-$75 Shipping Fee Discontinuity",
            "total_shipping_dropouts": 2143,
            "sub75_shipping_dropouts": 1567,
            "sub75_dropoff_rate": "24.20%",
            "free_shipping_dropoff": "6.16%",
            "elasticity_or_10pct": "1.493 (p < 10^-100)",
            "threshold_cliff": "16.14% drop-off at $60-$74.99 vs 6.16% at $75-$90",
            "backtracking_rate": "9.29% at $60-$74.99 vs 4.75% at $75-$90",
            "interpretation": "Shipping review abandonment escalates sharply when shipping fees impose a heavy proportional surcharge on low-ticket carts. Near-threshold carts exhibit elevated backtracking to seek free shipping."
        },
        "payment": {
            "title": "Payment Decline Recovery & Permanent Losses",
            "failed_sessions": 857,
            "decline_rate": "6.52% of payment attempts",
            "recovery_rate": "52.28% (448 sessions recovered)",
            "unrecovered_sessions": "409 sessions permanently lost",
            "immediate_exit_rate": "25.90% exit upon first decline",
            "worst_instrument": "Net Banking (11.64% decline rate) & Debit Cards (8.72%)",
            "best_instrument": "Digital Wallets (3.41% decline rate)",
            "interpretation": "47.72% of payment-failed sessions never recover, resulting in 409 permanently lost checkout orders due to lack of immediate alternative payment guidance."
        },
        "promo": {
            "title": "Promo Code Rejection Attrition",
            "invalid_promo_sessions": 1423,
            "checkout_rate_invalid": "41.25%",
            "checkout_rate_valid": "62.38%",
            "checkout_rate_nopromo": "62.57%",
            "progression_deficit": "-21.32 pp drop in checkout initiation (p < 10^-50)",
            "lost_cart_sessions": "836 cart dropouts",
            "cvr_impact": "26.56% session CVR vs 40.32% for non-promo carts",
            "interpretation": "Invalid promo code errors are strongly associated with pre-checkout cart exit. This reflects a mix of negative feedback friction and price-sensitive coupon hunter selection bias."
        },
        "browsing": {
            "title": "Browsing Depth & Intent Dynamics (Canonical Series)",
            "tiers": [
                {"tier": "1 View (Focused/Bouncer)", "sessions": 54075, "traffic_share": "45.06%", "cart_add_rate": "30.90%", "session_cvr": "12.44%", "cart_to_purchase": "40.27%"},
                {"tier": "2–3 Views (Moderate)", "sessions": 44842, "traffic_share": "37.37%", "cart_add_rate": "26.69%", "session_cvr": "10.51%", "cart_to_purchase": "39.39%"},
                {"tier": "4–6 Views (Extensive)", "sessions": 16713, "traffic_share": "13.93%", "cart_add_rate": "19.58%", "session_cvr": "7.68%", "cart_to_purchase": "39.23%"},
                {"tier": "7+ Views (Comparison)", "sessions": 4370, "traffic_share": "3.64%", "cart_add_rate": "9.20%", "session_cvr": "3.66%", "cart_to_purchase": "39.80%"}
            ],
            "correlation": "r = -0.0690 (Point-biserial), p = 1.50e-126",
            "interpretation": "Browsing depth exhibits a monotonic conversion decay, but the linear association is weak (|r| < 0.10). Notably, cart-to-purchase CVR remains invariant (~39.8%), demonstrating that conversion decay operates through lower cart addition rates rather than checkout friction."
        }
    },
    "hypothesis_scorecard": [
        {
            "id": "H1",
            "title": "Mobile Checkout Friction",
            "statement": "Mobile checkout completion is significantly lower than desktop due to form friction.",
            "verdict": "Supported",
            "status_color": "green",
            "evidence": "Mobile address pass rate is 79.18% vs Desktop 87.07% (Adj OR = 0.5704, p = 4.48e-37). Mobile dwell time is +21.6% longer (45s vs 37s).",
            "caveat": "Friction concentrates specifically at the address entry stage; payment execution pass rates are comparable across devices."
        },
        {
            "id": "H2",
            "title": "Session Dwell Time & Conversion",
            "statement": "Longer session duration is positively associated with purchase completion.",
            "verdict": "Not Supported (Confounded)",
            "status_color": "red",
            "evidence": "While converting sessions have higher total dwell time (median 200s vs 49s), this is an artifact of path length (more steps). Step-level dwell time is negatively associated with conversion.",
            "caveat": "Total duration was heavily confounded by funnel progression depth."
        },
        {
            "id": "H3",
            "title": "Shipping Fee Sticker Shock",
            "statement": "Higher shipping cost relative to cart value increases checkout drop-off.",
            "verdict": "Supported",
            "status_color": "green",
            "evidence": "Shipping abandonment jumps from 6.16% for free shipping to 27.49% for sub-$40 carts (OR_10% = 1.4927, p < 10^-100).",
            "caveat": "Observed price elasticity; customer willingness to wait for economy delivery was not directly measured."
        },
        {
            "id": "H4",
            "title": "Payment Failure Recovery Drag",
            "statement": "Payment gateway failures cause permanent session abandonment.",
            "verdict": "Supported",
            "status_color": "green",
            "evidence": "47.72% of payment-failed sessions never recover, causing 409 permanently lost checkout sessions. Net banking declines reach 11.64%.",
            "caveat": "52.28% do recover via retries and method switches without product intervention."
        },
        {
            "id": "H5",
            "title": "Promotional Code Validation Friction",
            "statement": "Invalid promo code errors lead to cart abandonment.",
            "verdict": "Supported (Observational)",
            "status_color": "green",
            "evidence": "Invalid promo carts advance to checkout at only 41.25% vs 62.57% for non-promo carts (Chi2 = 244.1, p < 10^-50).",
            "caveat": "Subject to coupon-hunter selection bias (deal-seekers may be inherently less committed to purchase)."
        },
        {
            "id": "H6",
            "title": "Customer Maturity & Account Advantage",
            "statement": "Returning customers convert at significantly higher rates than first-time visitors.",
            "verdict": "Supported",
            "status_color": "green",
            "evidence": "Returning customers achieve 13.46% CVR vs 9.08% for new visitors (Adj OR = 1.5518, p < 10^-100), with advantages compounding across cart (+4.76pp) and address (+7.70pp).",
            "caveat": "Observational cohort gap; may reflect customer brand affinity rather than account UI features."
        },
        {
            "id": "H7",
            "title": "Browsing Depth & Discovery Conversion",
            "statement": "Deeper product browsing is positively correlated with purchase intent.",
            "verdict": "Not Supported (Monotonic Decay)",
            "status_color": "red",
            "evidence": "Conversion declines monotonically from 12.44% (1 view) to 3.66% (7+ views). Weak linear correlation (r = -0.0690, p = 1.50e-126).",
            "caveat": "Decay is driven by lower cart formation rate (30.9% -> 9.2%), while cart-to-purchase conversion is flat (~39.8%)."
        },
        {
            "id": "H8",
            "title": "Acquisition Channel Quality Disparities",
            "statement": "Paid acquisition traffic experiences higher bounce rates than direct and organic search.",
            "verdict": "Supported",
            "status_color": "green",
            "evidence": "Direct traffic converts at 14.12% and Organic Search at 11.85%, while Paid Social converts at 8.42% and Paid Search at 9.61% (Chi2 = 218.4, p < 10^-40).",
            "caveat": "Reflects inbound search intent differences across acquisition sources."
        },
        {
            "id": "H9",
            "title": "High-Value Cart Payment Friction",
            "statement": "High-ticket orders experience elevated payment stage drop-off.",
            "verdict": "Supported",
            "status_color": "green",
            "evidence": "Baskets >$300 drop off at 8.4% at payment vs 4.8% for sub-$50 carts (Chi2 = 23.29, p < 0.0001). Credit card declines on >$150 carts reach 7.52%.",
            "caveat": "Driven by banking risk algorithms and single-transaction card limits."
        },
        {
            "id": "H10",
            "title": "Checkout Backtracking & Threshold Seeking",
            "statement": "Checkout backtracking is associated with free shipping threshold qualification.",
            "verdict": "Supported (Consistent)",
            "status_color": "green",
            "evidence": "Backtracking from checkout back to cart/browsing peaks at 9.29% for near-threshold carts ($60-$74.99), double the rate of qualifying carts (4.75%).",
            "caveat": "Behavior is consistent with threshold-seeking product additions; clickstream logs do not record explicit search queries."
        }
    ],
    "experiments": [
        {
            "id": "EXP-01",
            "name": "Mobile Address Autocomplete & Input Optimization",
            "problem_id": "PROB-01",
            "target_stage": "Checkout — Address Entry",
            "candidate_intervention": "Real-time Google Places / Postal API address autocomplete dropdown, HTML5 mobile numeric keypads, and inline onBlur field validation.",
            "control": "Existing multi-field manual address entry form.",
            "treatment": "Single-line street address search field with verified suggestion dropdown and automated city/state/zip auto-fill.",
            "hypothesis": "If providing real-time address autocomplete reduces mobile touchscreen typing burden, then mobile checkout progression from address entry to shipping review will increase relative to control, without increasing downstream delivery validation errors.",
            "primary_metric": "Mobile Address Stage Pass Rate (passed_address_pct)",
            "metric_formula": "Mobile Sessions reaching shipping_view / Mobile Sessions reaching address_entry",
            "baseline": "79.18%",
            "mde": "+4.0% relative (p2 = 82.35%)",
            "sample_per_arm": "2,430 mobile address sessions",
            "total_sample": "4,860 mobile address sessions",
            "daily_traffic": "147.1 sessions/day",
            "runtime": "33 days (~5 weeks)",
            "decision_rule": "SHIP if Primary Metric increases by >= +2.5% (p < 0.05) and Address Validation Error Rate increases by <= 0.10 pp. ITERATE if lift is +1.0% to +2.4% (p >= 0.05). ROLLBACK if pass rate drops or error rate increases > 0.20 pp.",
            "secondary_metrics": ["Mobile Address Dwell Time (target <38s)", "Mobile Full-Funnel Purchase CVR"],
            "guardrails": ["Address Validation Error Rate (<= +0.10 pp)", "Autocomplete API Response Latency (p95 <= 200ms)"]
        },
        {
            "id": "EXP-02",
            "name": "Dynamic Free Shipping Progress Bar & Add-On Suggestions",
            "problem_id": "PROB-02",
            "target_stage": "Cart & Checkout — Shipping Review",
            "candidate_intervention": "Interactive Free Shipping progress bar on cart drawer ('Add $14.50 for FREE Shipping!') paired with 1-click low-cost catalog add-on suggestions for $50-$74.99 carts.",
            "control": "Static cart summary calculating delivery fee only at step 2 of checkout.",
            "treatment": "Dynamic progress bar indicating remaining spend for free delivery with 1-click add-on items.",
            "hypothesis": "If making the $75 free shipping threshold prominently visible in the cart alongside relevant low-cost add-ons reduces surprise shipping costs, then sub-$75 cart-to-purchase conversion will increase and sub-$75 basket sizes will expand relative to control without reducing net shipping margin contribution.",
            "primary_metric": "Sub-$75 Cart-to-Purchase Conversion Rate (sub75_cart_to_purchase_cvr)",
            "metric_formula": "Sub-$75 Cart Sessions Completing Purchase / Total Sub-$75 Cart Sessions",
            "baseline": "34.36%",
            "mde": "+7.5% relative (p2 = 36.93%)",
            "sample_per_arm": "5,423 sub-$75 cart sessions",
            "total_sample": "10,846 sub-$75 cart sessions",
            "daily_traffic": "144.1 sessions/day",
            "runtime": "75 days (~11 weeks)",
            "decision_rule": "SHIP if Sub-$75 Cart CVR increases by >= +5.0% (p < 0.05) and Net Shipping Contribution Margin remains within +- 2.0%. ITERATE if AOV expands >+$3.00 but CVR is neutral. ROLLBACK if net margin decreases > 3.0%.",
            "secondary_metrics": ["Sub-$75 Average Order Value (AOV)", "Shipping Review Abandonment Rate", "Threshold Crossing Rate"],
            "guardrails": ["Net Shipping Contribution Margin (+- 2.0%)", "Cart Abandonment on >=$75 Carts (neutral)"]
        },
        {
            "id": "EXP-03",
            "name": "Smart Payment Decline Recovery & Instant Alternative APM Prompt",
            "problem_id": "PROB-03",
            "target_stage": "Checkout — Payment Authorization",
            "candidate_intervention": "Contextual soft-decline recovery modal explaining the issue in consumer language with pre-configured 1-click Apple Pay, Google Pay, and saved method switching.",
            "control": "Standard red inline error message banner ('Payment authorization failed. Please try again').",
            "treatment": "Focused Smart Recovery Modal with 1-click Digital Wallet buttons and preserved checkout state.",
            "hypothesis": "If presenting customers who experience soft payment declines with clear recovery guidance and instant 1-click alternative payment methods reduces exit hesitation, then payment failure recovery rates will increase relative to control, recovering lost orders.",
            "primary_metric": "Payment Failure Recovery Rate (payment_recovery_rate_pct)",
            "metric_formula": "Failed Payment Sessions Successfully Completing Order / Total Failed Payment Sessions",
            "baseline": "52.28%",
            "mde": "+15.0% relative (p2 = 60.12%)",
            "sample_per_arm": "628 failed payment sessions",
            "total_sample": "1,256 failed payment sessions",
            "daily_traffic": "9.5 sessions/day",
            "runtime": "132 days (~18.8 weeks / 19 weeks; Accelerated +20% MDE option: 75 days)",
            "decision_rule": "SHIP if Recovery Rate increases by >= +10.0% (p < 0.05) and Duplicate Charge Incidents = 0. ITERATE if recovery lift is +5.0% to +9.9% (p >= 0.05). ROLLBACK on any double-charge incident or customer dispute rate > 0.5%.",
            "secondary_metrics": ["Payment Method Switch Rate", "Immediate Exit Rate Post-Decline (<18%)"],
            "guardrails": ["Zero Duplicate Charge Incidents (0.00%)", "Fraud Dispute / Chargeback Rate (<= 0.5%)"]
        },
        {
            "id": "EXP-04",
            "name": "Collapsible Promo Drawer & Inline Store Deals",
            "problem_id": "PROB-04",
            "target_stage": "Shopping Cart — Promo Input",
            "candidate_intervention": "Collapsible promo code link ('+ Have a promo code?'), real-time asynchronous validation, empathetic inline error messaging, and verified store deals carousel.",
            "control": "Prominently exposed empty promo text field with standard red error messages.",
            "treatment": "Collapsed text link expanding to async validation box and active eligible store deals carousel.",
            "hypothesis": "If de-emphasizing the empty promo code input box reduces off-site coupon hunting while displaying verified store deals reduces rejection disappointment, then cart-to-checkout initiation will increase relative to control without inflating overall discount expenditure.",
            "primary_metric": "Cart-to-Checkout Initiation Rate (cart_to_checkout_rate_pct)",
            "metric_formula": "Cart Sessions reaching checkout_start / Total Sessions reaching add_to_cart",
            "baseline": "61.60%",
            "mde": "+3.0% relative (p2 = 63.45%)",
            "sample_per_arm": "10,768 cart sessions",
            "total_sample": "21,536 cart sessions",
            "daily_traffic": "359.5 sessions/day",
            "runtime": "60 days (~9 weeks)",
            "decision_rule": "SHIP if Cart-to-Checkout Rate increases by >= +2.0% (p < 0.05) and Gross Discount Rate increases by <= 0.50 pp of GMV. ITERATE if progression improves but discount rate exceeds threshold. ROLLBACK on conversion decline or promo abuse.",
            "secondary_metrics": ["Invalid Promo Error Frequency (-50%)", "Overall Cart-to-Purchase CVR"],
            "guardrails": ["Gross Discount Expenditure Rate (<= +0.50 pp of GMV)", "Cart-to-Purchase CVR (neutral/positive)"]
        }
    ],
    "decision_framework": {
        "principles": [
            "Statistical Significance is a Necessary, but Not Sufficient, Condition to Ship.",
            "A feature shall NOT automatically ship simply because p < 0.05.",
            "Rollout decisions require satisfying Statistical Rigor, Practical Commercial Impact, and Guardrail Integrity simultaneously.",
            "All experiments represent proposed designs. No A/B test has been executed."
        ],
        "quadrants": [
            {"decision": "SHIP", "criteria": "Primary Metric is positive and statistically significant (p < 0.05), effect size meets commercial threshold, all guardrails healthy, zero SRM (p >= 0.001).", "action": "Gradual rollout (50% -> 75% -> 100%) over 7 days with telemetry monitoring."},
            {"decision": "ITERATE", "criteria": "Primary metric is directionally positive (0.05 <= p < 0.20) or statistically significant with minor guardrail friction (e.g. slight API latency increase).", "action": "Refine implementation (optimize caching, UI copy) and execute follow-up test."},
            {"decision": "ROLLBACK", "criteria": "Primary metric is statistically significantly negative (p < 0.05) or critical guardrail is severely breached (>3% margin loss, duplicate charge).", "action": "Immediate 0% feature flag disablement; execute engineering post-mortem."},
            {"decision": "INCONCLUSIVE", "criteria": "Primary metric delta is negligible (|Delta| < 0.5%, p > 0.30) after reaching 100% sample size; guardrails neutral.", "action": "Feature does not ship; archive learnings and redirect engineering resources."}
        ]
    },
    "traceability_sample": [
        {
            "problem_id": "PROB-01",
            "evidence": "Mobile Address Adj OR = 0.5704, 1,043.7 excess lost sessions",
            "objective": "OBJ-01 (+4.0% relative lift in mobile address pass rate)",
            "business_req": "BR-ADDR-01 (Reduce mobile address entry friction while preserving accuracy)",
            "functional_req": "FR-ADDR-101 (Address Autocomplete), FR-ADDR-102 (Mobile Keypads), FR-ADDR-103 (Inline Validation)",
            "nfr": "NFR-PERF-01 (API Latency p95 <= 200ms), NFR-ACC-02 (44px touch targets)",
            "user_story": "US-ADDR-01 (Mobile address autocomplete dropdown), US-ADDR-02 (Numeric keypads)",
            "acceptance_criteria": "AC-ADDR-01 (Dropdown display), AC-ADDR-02 (Auto-fill population)",
            "use_case": "UC-01 (Mobile Address Autocomplete Completion)",
            "experiment": "EXP-01 (Mobile Address Autocomplete)",
            "primary_kpi": "Mobile Address Pass Rate (79.18% -> 82.35%)"
        },
        {
            "problem_id": "PROB-02",
            "evidence": "Sub-$75 shipping drop-off reaches 24.20%, OR_10% = 1.493",
            "objective": "OBJ-02 (+7.5% relative lift in sub-$75 cart-to-purchase CVR)",
            "business_req": "BR-SHIP-01 (Communicate thresholds upfront and assist basket building)",
            "functional_req": "FR-SHIP-201 (Dynamic Progress Bar), FR-SHIP-202 (Add-On Carousel)",
            "nfr": "NFR-PERF-02 (DOM render <= 300ms), NFR-OBS-01 (Telemetry events)",
            "user_story": "US-SHIP-01 (Free shipping progress indicator and add-ons)",
            "acceptance_criteria": "AC-SHIP-01 (Progress calculation), AC-SHIP-02 (Threshold unlock)",
            "use_case": "UC-02 (Free Shipping Threshold Awareness)",
            "experiment": "EXP-02 (Shipping Threshold Progress Bar)",
            "primary_kpi": "Sub-$75 Cart-to-Purchase CVR (34.36% -> 36.93%)"
        },
        {
            "problem_id": "PROB-03",
            "evidence": "857 payment declines, 47.72% unrecovered, 409 lost sessions",
            "objective": "OBJ-03 (+15.0% relative lift in payment recovery rate)",
            "business_req": "BR-PAY-01 (Intelligent decline recovery and instant fallback)",
            "functional_req": "FR-PAY-301 (Decline Classification), FR-PAY-302 (Recovery Modal)",
            "nfr": "NFR-PERF-04 (Fallback timeout <= 3.0s), NFR-SEC-01 (PCI-DSS iframe)",
            "user_story": "US-PAY-01 (Decline guidance and 1-click digital wallet switch)",
            "acceptance_criteria": "AC-PAY-01 (Modal display), AC-PAY-02 (1-Click APM capture)",
            "use_case": "UC-03 (Payment Decline Recovery via Digital Wallet)",
            "experiment": "EXP-03 (Smart Payment Recovery Modal)",
            "primary_kpi": "Payment Failure Recovery Rate (52.28% -> 60.12%)"
        },
        {
            "problem_id": "PROB-04",
            "evidence": "Invalid promo carts drop -21.32pp in checkout progression (p < 10^-50)",
            "objective": "OBJ-04 (+3.0% relative lift in cart-to-checkout initiation)",
            "business_req": "BR-PROMO-01 (Frictionless promo interaction & deal transparency)",
            "functional_req": "FR-PROMO-401 (Collapsible Drawer), FR-PROMO-402 (Async Validation), FR-PROMO-403 (Deals Carousel)",
            "nfr": "NFR-PERF-03 (Validation latency <= 250ms), NFR-REL-02 (Graceful degradation)",
            "user_story": "US-PROMO-01 (Streamlined promo entry and store deals)",
            "acceptance_criteria": "AC-PROMO-01 (Drawer expansion), AC-PROMO-02 (Friendly error feedback)",
            "use_case": "UC-04 (Promo Code Entry & Inline Error Recovery)",
            "experiment": "EXP-04 (Collapsible Promo Drawer & Deals)",
            "primary_kpi": "Cart-to-Checkout Initiation Rate (61.60% -> 63.45%)"
        }
    ],
    "research_gaps": [
        {"gap": "Mobile Form Focus Keystrokes", "limitation": "Clickstream logs record stage dwell times, but do not capture field-level focus, keyboard switching, or zoom disruptions.", "protocol": "Moderated Usability Lab Testing (N = 12 smartphone participants) with screen-recorded think-aloud sessions."},
        {"gap": "Customer Perceived Shipping Value", "limitation": "Observational drop-off shows fee sensitivity, but cannot distinguish delivery cost objection from delivery speed dissatisfaction.", "protocol": "Exit-Intent Micro-Surveys (N = 500 responses) triggered upon cart/checkout exit."},
        {"gap": "Payment Error Mental Models", "limitation": "Logs capture decline error codes, but cannot observe whether users understood why the decline occurred.", "protocol": "Session Replay Video Audit (N = 100 failed checkout sessions) reviewing rage clicks and cursor hesitation."},
        {"gap": "Promo Code Acquisition Sourcing", "limitation": "Logs record invalid promo attempts, but cannot observe whether users searched coupon aggregators or browser extensions.", "protocol": "Customer Discovery Interviews (N = 15 cart abandoners) investigating coupon extension behaviors."},
        {"gap": "First-Time Buyer Trust Signals", "limitation": "Cohort analysis proves new visitor conversion drag, but cannot isolate brand trust from guest checkout friction.", "protocol": "Unmoderated Card Sorting & Tree Testing (N = 60 participants) testing trust badge placement."}
    ],
    "tech_stack": [
        {"category": "Data Generation & Modeling", "tools": "Python 3.11, NumPy, SciPy (Stochastic State Machine, 17 Data Quality Rules)"},
        {"category": "Analytical Processing", "tools": "DuckDB SQL, Pandas, Statsmodels (Logistic Regression, OLS, Mann-Whitney U, Chi-Square)"},
        {"category": "Experimentation Engine", "tools": "Statistical Power Analysis, Two-Sample Proportion Testing, MDE & Sample Planning"},
        {"category": "Product Strategy", "tools": "BRD, FRS, NFR, User Stories, Given/When/Then Acceptance Criteria, Full RTM"},
        {"category": "Frontend Architecture", "tools": "Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Lucide Icons"}
    ],
    "repo_artifacts": [
        {"title": "SQL Analytics Suite", "path": "sql/01_funnel_analysis.sql through 11_channel_deepdive.sql", "type": "SQL Scripts"},
        {"title": "Exploratory Analysis Notebook", "path": "notebooks/exploratory_analysis.ipynb", "type": "Jupyter Notebook"},
        {"title": "Data Dictionary & Model", "path": "docs/data-model.md & docs/data-dictionary.md", "type": "Documentation"},
        {"title": "Hypothesis Evaluation Framework", "path": "analysis/07_hypothesis_results.md", "type": "Analytical Report"},
        {"title": "Root-Cause Investigation", "path": "analysis/phase4_root_cause_summary.md", "type": "Diagnostic Report"},
        {"title": "Product Requirements (BRD/FRS)", "path": "product/business-requirements.md & functional-requirements.md", "type": "Product Specs"},
        {"title": "Experimentation Catalog", "path": "experimentation/experiment-catalog.md & power-analysis.md", "type": "Experiment Specs"}
    ]
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Successfully generated presentation dataset at: {OUTPUT_PATH}")
print(f"Total JSON Size: {os.path.getsize(OUTPUT_PATH):,} bytes")
