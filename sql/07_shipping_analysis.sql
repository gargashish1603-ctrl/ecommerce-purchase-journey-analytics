-- ==============================================================================
-- 07_shipping_analysis.sql
-- ShopSphere Phase 3: Shipping Fee Ratios & Shipping-Stage Drop-Off Dynamics
-- ==============================================================================

WITH shipping_sessions AS (
    SELECT
        session_id,
        cart_value,
        shipping_cost,
        CASE 
            WHEN shipping_cost = 0.0 THEN 'Free Shipping ($0)'
            WHEN (shipping_cost / NULLIF(cart_value, 0)) < 0.08 THEN 'Low Ratio (<8%)'
            WHEN (shipping_cost / NULLIF(cart_value, 0)) BETWEEN 0.08 AND 0.15 THEN 'Moderate Ratio (8-15%)'
            WHEN (shipping_cost / NULLIF(cart_value, 0)) BETWEEN 0.15 AND 0.25 THEN 'High Ratio (15-25%)'
            ELSE 'Severe Ratio (>25%)'
        END AS shipping_burden_tier,
        (shipping_cost / NULLIF(cart_value, 0)) AS ship_ratio
    FROM events
    WHERE event_type = 'shipping_view'
),
shipping_outcomes AS (
    SELECT
        ss.session_id,
        ss.shipping_burden_tier,
        ss.shipping_cost,
        ss.cart_value,
        ss.ship_ratio,
        s.is_purchased,
        s.dropoff_stage
    FROM shipping_sessions ss
    JOIN sessions s ON ss.session_id = s.session_id
)
SELECT
    shipping_burden_tier,
    COUNT(*) AS shipping_view_sessions,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_pct,
    ROUND(AVG(cart_value), 2) AS avg_cart_value,
    ROUND(AVG(shipping_cost), 2) AS avg_shipping_cost,
    ROUND(AVG(ship_ratio) * 100.0, 2) AS avg_shipping_ratio_pct,
    SUM(CASE WHEN dropoff_stage = 'shipping' THEN 1 ELSE 0 END) AS abandoned_at_shipping,
    ROUND(SUM(CASE WHEN dropoff_stage = 'shipping' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS shipping_dropoff_rate_pct,
    SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) AS final_purchases,
    ROUND(SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS shipping_to_order_cvr_pct
FROM shipping_outcomes
GROUP BY shipping_burden_tier
ORDER BY avg_shipping_ratio_pct ASC;
