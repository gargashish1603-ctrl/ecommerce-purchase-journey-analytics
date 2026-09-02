-- ==============================================================================
-- 03_device_analysis.sql
-- ShopSphere Phase 3: Cross-Device Funnel Comparison & Conversion Disparities
-- ==============================================================================

WITH device_funnel AS (
    SELECT
        device_type,
        COUNT(DISTINCT session_id) AS total_sessions,
        COUNT(DISTINCT CASE WHEN reached_cart = TRUE THEN session_id END) AS cart_sessions,
        COUNT(DISTINCT CASE WHEN reached_checkout = TRUE THEN session_id END) AS checkout_sessions,
        COUNT(DISTINCT CASE WHEN reached_payment = TRUE THEN session_id END) AS payment_sessions,
        COUNT(DISTINCT CASE WHEN is_purchased = TRUE THEN session_id END) AS converted_sessions
    FROM sessions
    GROUP BY device_type
)
SELECT
    device_type,
    total_sessions,
    ROUND(total_sessions * 100.0 / SUM(total_sessions) OVER (), 2) AS traffic_share_pct,
    cart_sessions,
    ROUND(cart_sessions * 100.0 / total_sessions, 2) AS cart_rate_pct,
    checkout_sessions,
    ROUND(checkout_sessions * 100.0 / cart_sessions, 2) AS cart_to_checkout_rate_pct,
    payment_sessions,
    ROUND(payment_sessions * 100.0 / checkout_sessions, 2) AS checkout_to_payment_rate_pct,
    converted_sessions,
    ROUND(converted_sessions * 100.0 / payment_sessions, 2) AS payment_to_order_rate_pct,
    ROUND(converted_sessions * 100.0 / total_sessions, 2) AS overall_session_cvr_pct
FROM device_funnel
ORDER BY total_sessions DESC;
