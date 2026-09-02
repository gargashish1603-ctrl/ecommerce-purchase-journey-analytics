-- ==============================================================================
-- 11_sequence_analysis.sql
-- ShopSphere Phase 3: Behavioral Sequence Mining & Common Event Trajectories
-- ==============================================================================

WITH session_event_strings AS (
    SELECT
        session_id,
        STRING_AGG(event_type, ' -> ' ORDER BY event_sequence) AS full_journey_path,
        MAX(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) AS is_purchased
    FROM (
        SELECT 
            e.session_id, 
            e.event_type, 
            e.event_sequence, 
            s.is_purchased
        FROM events e
        JOIN sessions s ON e.session_id = s.session_id
    ) t
    GROUP BY session_id
)
-- Top 10 Most Common Converted Journey Paths
SELECT
    'Converted Paths' AS path_category,
    full_journey_path,
    COUNT(*) AS session_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sessions WHERE is_purchased = TRUE), 2) AS share_of_converted_sessions_pct
FROM session_event_strings
WHERE is_purchased = 1
GROUP BY full_journey_path
ORDER BY session_count DESC
LIMIT 10;
