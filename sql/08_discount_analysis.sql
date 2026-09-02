-- ==============================================================================
-- 08_discount_analysis.sql
-- ShopSphere Phase 3: Promotional Code Usage, Validation Errors & Conversion
-- ==============================================================================

WITH promo_sessions AS (
    SELECT
        s.session_id,
        s.reached_cart,
        s.reached_checkout,
        s.is_purchased,
        s.final_cart_value,
        MAX(CASE WHEN e.event_type = 'promo_applied' THEN 1 ELSE 0 END) AS has_promo_attempt,
        MAX(CASE WHEN e.event_type = 'promo_applied' AND e.error_code IS NULL THEN 1 ELSE 0 END) AS has_valid_promo,
        MAX(CASE WHEN e.event_type = 'promo_applied' AND e.error_code IS NOT NULL THEN 1 ELSE 0 END) AS has_invalid_promo,
        MAX(COALESCE(e.discount_amount, 0)) AS max_discount_amount
    FROM sessions s
    LEFT JOIN events e ON s.session_id = e.session_id
    WHERE s.reached_cart = TRUE
    GROUP BY s.session_id, s.reached_cart, s.reached_checkout, s.is_purchased, s.final_cart_value
),
promo_categorized AS (
    SELECT
        session_id,
        reached_checkout,
        is_purchased,
        final_cart_value,
        max_discount_amount,
        CASE
            WHEN has_promo_attempt = 0 THEN 'No Promo Attempted'
            WHEN has_valid_promo = 1 THEN 'Valid Promo Applied'
            ELSE 'Invalid / Expired Promo Attempted'
        END AS promo_status
    FROM promo_sessions
)
SELECT
    promo_status,
    COUNT(*) AS cart_sessions,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_pct,
    SUM(CASE WHEN reached_checkout = TRUE THEN 1 ELSE 0 END) AS checkout_starts,
    ROUND(SUM(CASE WHEN reached_checkout = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cart_to_checkout_pct,
    SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) AS completed_orders,
    ROUND(SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cart_to_purchase_cvr_pct,
    ROUND(AVG(final_cart_value), 2) AS avg_cart_value,
    ROUND(AVG(CASE WHEN max_discount_amount > 0 THEN max_discount_amount END), 2) AS avg_discount_saved
FROM promo_categorized
GROUP BY promo_status;
