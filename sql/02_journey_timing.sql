-- ==============================================================================
-- 02_journey_timing.sql
-- ShopSphere Phase 3: Stage Dwell Times, Hesitation Latency & Checkout Durations
-- ==============================================================================

-- 1. Step Dwell Times by Event Type (Median, IQR, Mean, Max)
SELECT
    event_type,
    COUNT(*) AS event_occurrences,
    ROUND(AVG(time_since_previous_event), 2) AS avg_duration_sec,
    MEDIAN(time_since_previous_event) AS median_duration_sec,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY time_since_previous_event) AS p25_duration_sec,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY time_since_previous_event) AS p75_duration_sec,
    (PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY time_since_previous_event) - 
     PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY time_since_previous_event)) AS iqr_duration_sec,
    MAX(time_since_previous_event) AS max_duration_sec
FROM events
WHERE event_sequence > 1
GROUP BY event_type
ORDER BY median_duration_sec DESC;

-- 2. Total Checkout Duration by Conversion Status (Converted vs Abandoned)
SELECT
    is_purchased,
    COUNT(*) AS session_count,
    ROUND(AVG(session_duration_seconds), 2) AS avg_total_duration_sec,
    MEDIAN(session_duration_seconds) AS median_total_duration_sec,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY session_duration_seconds) AS p25_total_duration_sec,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY session_duration_seconds) AS p75_total_duration_sec
FROM sessions
WHERE reached_checkout = TRUE
GROUP BY is_purchased;

-- 3. Address Entry Dwell Time by Device Category
SELECT
    e.device_type,
    COUNT(*) AS address_events,
    ROUND(AVG(e.time_since_previous_event), 2) AS avg_address_dwell_sec,
    MEDIAN(e.time_since_previous_event) AS median_address_dwell_sec,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY e.time_since_previous_event) AS p25_address_dwell_sec,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY e.time_since_previous_event) AS p75_address_dwell_sec
FROM events e
WHERE e.event_type = 'address_entry'
GROUP BY e.device_type;
