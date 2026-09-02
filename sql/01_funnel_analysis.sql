-- ==============================================================================
-- 01_funnel_analysis.sql
-- ShopSphere Phase 3: Macro & Micro Funnel Stage Progression & Drop-Off Analysis
-- ==============================================================================

-- 1. Macro Funnel Event Reach & Progression
WITH funnel_stages AS (
    SELECT
        COUNT(DISTINCT session_id) AS total_sessions,
        COUNT(DISTINCT CASE WHEN event_type = 'product_view' THEN session_id END) AS reached_product_view,
        COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN session_id END) AS reached_cart,
        COUNT(DISTINCT CASE WHEN event_type = 'cart_view' THEN session_id END) AS reached_cart_view,
        COUNT(DISTINCT CASE WHEN event_type = 'checkout_start' THEN session_id END) AS reached_checkout,
        COUNT(DISTINCT CASE WHEN event_type = 'address_entry' THEN session_id END) AS reached_address,
        COUNT(DISTINCT CASE WHEN event_type = 'shipping_view' THEN session_id END) AS reached_shipping,
        COUNT(DISTINCT CASE WHEN event_type = 'payment_select' THEN session_id END) AS reached_payment_select,
        COUNT(DISTINCT CASE WHEN event_type = 'payment_attempt' THEN session_id END) AS reached_payment_attempt,
        COUNT(DISTINCT CASE WHEN event_type = 'payment_success' THEN session_id END) AS reached_payment_success,
        COUNT(DISTINCT CASE WHEN event_type = 'order_completed' THEN session_id END) AS reached_purchase
    FROM events
)
SELECT
    '1. Session Start' AS funnel_stage, total_sessions AS sessions_reached, 100.0 AS stage_conversion_pct, 100.0 AS cumulative_conversion_pct, 0 AS dropoff_volume, 0.0 AS dropoff_rate_pct FROM funnel_stages
UNION ALL
SELECT
    '2. Product View', reached_product_view, ROUND(reached_product_view * 100.0 / total_sessions, 2), ROUND(reached_product_view * 100.0 / total_sessions, 2), (total_sessions - reached_product_view), ROUND((total_sessions - reached_product_view) * 100.0 / total_sessions, 2) FROM funnel_stages
UNION ALL
SELECT
    '3. Add to Cart', reached_cart, ROUND(reached_cart * 100.0 / reached_product_view, 2), ROUND(reached_cart * 100.0 / total_sessions, 2), (reached_product_view - reached_cart), ROUND((reached_product_view - reached_cart) * 100.0 / reached_product_view, 2) FROM funnel_stages
UNION ALL
SELECT
    '4. Cart View', reached_cart_view, ROUND(reached_cart_view * 100.0 / reached_cart, 2), ROUND(reached_cart_view * 100.0 / total_sessions, 2), (reached_cart - reached_cart_view), ROUND((reached_cart - reached_cart_view) * 100.0 / reached_cart, 2) FROM funnel_stages
UNION ALL
SELECT
    '5. Checkout Start', reached_checkout, ROUND(reached_checkout * 100.0 / reached_cart, 2), ROUND(reached_checkout * 100.0 / total_sessions, 2), (reached_cart - reached_checkout), ROUND((reached_cart - reached_checkout) * 100.0 / reached_cart, 2) FROM funnel_stages
UNION ALL
SELECT
    '6. Address Entry', reached_address, ROUND(reached_address * 100.0 / reached_checkout, 2), ROUND(reached_address * 100.0 / total_sessions, 2), (reached_checkout - reached_address), ROUND((reached_checkout - reached_address) * 100.0 / reached_checkout, 2) FROM funnel_stages
UNION ALL
SELECT
    '7. Shipping View', reached_shipping, ROUND(reached_shipping * 100.0 / reached_address, 2), ROUND(reached_shipping * 100.0 / total_sessions, 2), (reached_address - reached_shipping), ROUND((reached_address - reached_shipping) * 100.0 / reached_address, 2) FROM funnel_stages
UNION ALL
SELECT
    '8. Payment Selection', reached_payment_select, ROUND(reached_payment_select * 100.0 / reached_shipping, 2), ROUND(reached_payment_select * 100.0 / total_sessions, 2), (reached_shipping - reached_payment_select), ROUND((reached_shipping - reached_payment_select) * 100.0 / reached_shipping, 2) FROM funnel_stages
UNION ALL
SELECT
    '9. Payment Attempt', reached_payment_attempt, ROUND(reached_payment_attempt * 100.0 / reached_payment_select, 2), ROUND(reached_payment_attempt * 100.0 / total_sessions, 2), (reached_payment_select - reached_payment_attempt), ROUND((reached_payment_select - reached_payment_attempt) * 100.0 / reached_payment_select, 2) FROM funnel_stages
UNION ALL
SELECT
    '10. Payment Success', reached_payment_success, ROUND(reached_payment_success * 100.0 / reached_payment_attempt, 2), ROUND(reached_payment_success * 100.0 / total_sessions, 2), (reached_payment_attempt - reached_payment_success), ROUND((reached_payment_attempt - reached_payment_success) * 100.0 / reached_payment_attempt, 2) FROM funnel_stages
UNION ALL
SELECT
    '11. Order Completed', reached_purchase, ROUND(reached_purchase * 100.0 / reached_payment_success, 2), ROUND(reached_purchase * 100.0 / total_sessions, 2), (reached_payment_success - reached_purchase), ROUND((reached_payment_success - reached_purchase) * 100.0 / reached_payment_success, 2) FROM funnel_stages;
