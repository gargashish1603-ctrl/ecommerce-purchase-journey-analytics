-- ==============================================================================
-- 04_customer_analysis.sql
-- ShopSphere Phase 3: New vs. Returning Customer Cohort Funnel Diagnostics
-- ==============================================================================

WITH cohort_funnel AS (
    SELECT
        customer_type,
        COUNT(DISTINCT session_id) AS total_sessions,
        COUNT(DISTINCT customer_id) AS unique_customers,
        COUNT(DISTINCT CASE WHEN reached_cart = TRUE THEN session_id END) AS cart_sessions,
        COUNT(DISTINCT CASE WHEN reached_checkout = TRUE THEN session_id END) AS checkout_sessions,
        COUNT(DISTINCT CASE WHEN reached_payment = TRUE THEN session_id END) AS payment_sessions,
        COUNT(DISTINCT CASE WHEN is_purchased = TRUE THEN session_id END) AS converted_sessions,
        AVG(final_cart_value) AS avg_cart_val,
        AVG(session_duration_seconds) AS avg_duration_sec
    FROM sessions
    GROUP BY customer_type
)
SELECT
    customer_type,
    total_sessions,
    unique_customers,
    ROUND(total_sessions * 1.0 / unique_customers, 2) AS sessions_per_customer,
    ROUND(cart_sessions * 100.0 / total_sessions, 2) AS cart_rate_pct,
    ROUND(checkout_sessions * 100.0 / cart_sessions, 2) AS cart_to_checkout_rate_pct,
    ROUND(payment_sessions * 100.0 / checkout_sessions, 2) AS checkout_to_payment_rate_pct,
    ROUND(converted_sessions * 100.0 / total_sessions, 2) AS overall_cvr_pct,
    ROUND(avg_cart_val, 2) AS avg_cart_value,
    ROUND(avg_duration_sec, 2) AS avg_duration_seconds
FROM cohort_funnel;
