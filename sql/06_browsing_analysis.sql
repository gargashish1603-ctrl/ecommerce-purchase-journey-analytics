-- ==============================================================================
-- 06_browsing_analysis.sql
-- ShopSphere Phase 3: Browsing Depth (Product Views) vs Conversion Progression
-- ==============================================================================

WITH session_pv_counts AS (
    SELECT
        s.session_id,
        s.reached_cart,
        s.reached_checkout,
        s.is_purchased,
        s.session_duration_seconds,
        COUNT(CASE WHEN e.event_type = 'product_view' THEN 1 END) AS product_view_count
    FROM sessions s
    LEFT JOIN events e ON s.session_id = e.session_id
    GROUP BY s.session_id, s.reached_cart, s.reached_checkout, s.is_purchased, s.session_duration_seconds
),
binned_browsing AS (
    SELECT
        session_id,
        reached_cart,
        reached_checkout,
        is_purchased,
        session_duration_seconds,
        product_view_count,
        CASE
            WHEN product_view_count = 1 THEN '1 View (Bouncer/Fast)'
            WHEN product_view_count BETWEEN 2 AND 3 THEN '2-3 Views (Focused)'
            WHEN product_view_count BETWEEN 4 AND 6 THEN '4-6 Views (Moderate)'
            ELSE '7+ Views (Extensive/Comparison)'
        END AS browsing_tier
    FROM session_pv_counts
)
SELECT
    browsing_tier,
    COUNT(*) AS total_sessions,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS session_share_pct,
    SUM(CASE WHEN reached_cart = TRUE THEN 1 ELSE 0 END) AS cart_sessions,
    ROUND(SUM(CASE WHEN reached_cart = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cart_addition_rate_pct,
    SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) AS converted_sessions,
    ROUND(SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS purchase_cvr_pct,
    ROUND(AVG(session_duration_seconds), 2) AS avg_duration_sec,
    ROUND(MEDIAN(session_duration_seconds), 2) AS median_duration_sec
FROM binned_browsing
GROUP BY browsing_tier
ORDER BY MIN(product_view_count);
