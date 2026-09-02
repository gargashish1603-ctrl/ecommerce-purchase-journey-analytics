-- ==============================================================================
-- 05_channel_analysis.sql
-- ShopSphere Phase 3: Traffic Acquisition Channel Performance & Monetization
-- ==============================================================================

SELECT
    acquisition_channel,
    COUNT(DISTINCT session_id) AS total_sessions,
    ROUND(COUNT(DISTINCT session_id) * 100.0 / SUM(COUNT(DISTINCT session_id)) OVER (), 2) AS traffic_share_pct,
    COUNT(DISTINCT CASE WHEN reached_cart = TRUE THEN session_id END) AS cart_sessions,
    ROUND(COUNT(DISTINCT CASE WHEN reached_cart = TRUE THEN session_id END) * 100.0 / COUNT(DISTINCT session_id), 2) AS cart_rate_pct,
    COUNT(DISTINCT CASE WHEN reached_checkout = TRUE THEN session_id END) AS checkout_sessions,
    ROUND(COUNT(DISTINCT CASE WHEN reached_checkout = TRUE THEN session_id END) * 100.0 / NULLIF(COUNT(DISTINCT CASE WHEN reached_cart = TRUE THEN session_id END), 0), 2) AS checkout_rate_pct,
    COUNT(DISTINCT CASE WHEN is_purchased = TRUE THEN session_id END) AS converted_sessions,
    ROUND(COUNT(DISTINCT CASE WHEN is_purchased = TRUE THEN session_id END) * 100.0 / COUNT(DISTINCT session_id), 2) AS overall_cvr_pct,
    ROUND(AVG(CASE WHEN is_purchased = TRUE THEN final_cart_value END), 2) AS aov_converted,
    ROUND(SUM(CASE WHEN is_purchased = TRUE THEN final_cart_value ELSE 0 END), 2) AS total_revenue_generated
FROM sessions
GROUP BY acquisition_channel
ORDER BY total_revenue_generated DESC;
