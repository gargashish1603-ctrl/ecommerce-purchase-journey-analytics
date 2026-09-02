-- ==============================================================================
-- 10_abandonment_analysis.sql
-- ShopSphere Phase 3: Final Journey Abandonment Stages & Cohort Profiles
-- ==============================================================================

SELECT
    dropoff_stage,
    COUNT(*) AS abandoned_sessions,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_of_total_traffic_pct,
    ROUND(COUNT(*) * 100.0 / SUM(CASE WHEN dropoff_stage != 'converted' THEN COUNT(*) ELSE 0 END) OVER (), 2) AS share_of_abandoned_traffic_pct,
    ROUND(AVG(session_duration_seconds), 2) AS avg_duration_sec,
    ROUND(MEDIAN(session_duration_seconds), 2) AS median_duration_sec,
    ROUND(AVG(final_cart_value), 2) AS avg_final_cart_value,
    ROUND(SUM(CASE WHEN device_type = 'mobile' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS mobile_share_pct,
    ROUND(SUM(CASE WHEN customer_type = 'new' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS new_customer_share_pct
FROM sessions
GROUP BY dropoff_stage
ORDER BY 
    CASE dropoff_stage
        WHEN 'browsing' THEN 1
        WHEN 'cart' THEN 2
        WHEN 'address' THEN 3
        WHEN 'shipping' THEN 4
        WHEN 'payment' THEN 5
        WHEN 'converted' THEN 6
        ELSE 7
    END;
