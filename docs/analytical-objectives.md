# Analytical Objectives & Research Questions

This document outlines the core investigative objectives and analytical research questions that will guide the SQL diagnostics, Python statistical evaluations, and exploratory analyses. The objective is to formulate precise, testable questions without pre-judging or assuming the empirical outcome.

---

## 1. Conversion Funnel & Stage-Level Drop-Off
- **Q1.1 (Macro Funnel):** What is the baseline progression rate across each milestone of the ShopSphere purchase funnel (`Session Start` → `Product View` → `Add to Cart` → `Cart View` → `Checkout Start` → `Address Entry` → `Shipping View` → `Payment Selection` → `Payment Attempt` → `Purchase`)?
- **Q1.2 (Greatest Attrition):** Which specific transition step exhibits the highest absolute drop-off volume, and which exhibits the highest percentage loss?
- **Q1.3 (Micro-Checkout Funnel):** Once a customer initiates checkout (`Checkout Start`), where is the primary attrition point (Address Entry, Shipping Selection, or Payment Execution)?

---

## 2. Customer Cohort & Acquisition Behavior
- **Q2.1 (New vs. Returning Dynamics):** How do new visitors differ from returning customers in terms of cart addition rates, checkout initiation rates, and final checkout completion rates?
- **Q2.2 (Browsing Depth & Intent):** What is the relationship between the number of product views prior to cart addition (browsing depth) and the likelihood of final order completion? Does heavy exploratory browsing indicate deliberation/friction or high intent?
- **Q2.3 (Channel Intent Disparities):** Do acquisition channels (Organic Search, Paid Search, Paid Social, Direct, Email/CRM, Affiliate) yield statistically distinct conversion rates and checkout drop-off patterns?

---

## 3. Device & Platform Behavioral Differences
- **Q3.1 (Device Conversion Variance):** Does checkout progression and final conversion differ significantly between Mobile and Desktop users?
- **Q3.2 (Stage-Specific Device Friction):** Are specific form-heavy checkout stages (such as Address Entry or Card Details Entry) disproportionately abandoned on mobile devices relative to desktop?
- **Q3.3 (Dwell Time Disparities by Device):** Do mobile users exhibit longer or shorter dwell times across individual checkout steps compared to desktop users?

---

## 4. Checkout Timing, Dwell Time & Friction
- **Q4.1 (Step Duration Profiling):** What is the typical (median / IQR) time spent by users at each stage of the checkout flow?
- **Q4.2 (Dwell Time vs. Abandonment):** Is excessive dwell time at specific checkout stages (e.g., Address Entry or Shipping Selection) positively correlated with journey abandonment?
- **Q4.3 (Fast Drop-Off vs. Hesitation):** Do users who abandon checkout exit immediately upon page load (instant bounce/cost shock) or after prolonged interaction (form fatigue/hesitation)?

---

## 5. Payment Failures, Retries & Recovery Dynamics
- **Q5.1 (Payment Failure Frequency):** What proportion of initial payment attempts result in failure or gateway errors across different payment methods?
- **Q5.2 (Retry Propensity):** Following an initial payment failure, what percentage of users attempt a retry versus immediately abandoning the session?
- **Q5.3 (Payment Method Switching):** How frequently do users switch to an alternative payment method (e.g., from Credit Card to Digital Wallet or BNPL) after experiencing a failure?
- **Q5.4 (Ultimate Recovery Rate):** What proportion of sessions that encounter at least one payment failure ultimately convert into a successful purchase?

---

## 6. Commercial Policy, Shipping Fees & Cart Value Elasticity
- **Q6.1 (Shipping Cost Sensitivity):** How does the ratio of shipping cost to total cart value (`shipping_cost / cart_value`) impact checkout abandonment rates at the shipping step?
- **Q6.2 (Cart Value Tiering):** Do high-value carts (e.g., high AOV orders) behave differently throughout the checkout funnel compared to low-value carts?
- **Q6.3 (Discount & Promo Code Interactions):** Does the application of a discount code impact cart-to-checkout progression or checkout completion rates? Does failure to validate a promo code correlate with elevated abandonment?

---

## 7. Journey Path & Behavioral Sequence Analysis
- **Q7.1 (Top Converting Paths):** What are the most common end-to-end event sequence paths that lead to successful purchases?
- **Q7.2 (Top Abandoning Paths):** What are the most frequent event trajectories leading up to session termination without purchase?
- **Q7.3 (Looping & Backtracking):** Do users frequently backtrack from checkout to cart or product pages, and how does this cyclical behavior impact conversion probability?
