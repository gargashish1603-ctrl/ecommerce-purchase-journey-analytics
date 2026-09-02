-- ==============================================================================
-- 09_payment_recovery.sql
-- ShopSphere Phase 3: Payment Failure Diagnositcs, Retries & Method Switching
-- ==============================================================================

-- 1. Gateway Authorization & Decline Rates by Payment Method
SELECT
    payment_method,
    COUNT(*) AS total_authorization_attempts,
    SUM(CASE WHEN event_type = 'payment_success' THEN 1 ELSE 0 END) AS successful_captures,
    ROUND(SUM(CASE WHEN event_type = 'payment_success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS auth_success_rate_pct,
    SUM(CASE WHEN event_type = 'payment_failed' THEN 1 ELSE 0 END) AS declined_attempts,
    ROUND(SUM(CASE WHEN event_type = 'payment_failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_rate_pct
FROM events
WHERE event_type IN ('payment_success', 'payment_failed')
GROUP BY payment_method
ORDER BY total_authorization_attempts DESC;

-- 2. Breakdown of Payment Failure Reasons
SELECT
    error_code,
    error_message,
    COUNT(*) AS failure_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_of_failures_pct
FROM events
WHERE event_type = 'payment_failed'
GROUP BY error_code, error_message
ORDER BY failure_count DESC;

-- 3. Payment Recovery Pathways and Outcomes
WITH session_payment_flow AS (
    SELECT
        s.session_id,
        s.is_purchased,
        COUNT(CASE WHEN e.event_type = 'payment_attempt' THEN 1 END) AS total_attempts,
        COUNT(CASE WHEN e.event_type = 'payment_failed' THEN 1 END) AS failure_count,
        COUNT(DISTINCT CASE WHEN e.event_type IN ('payment_select', 'payment_attempt') THEN e.payment_method END) AS distinct_methods_used
    FROM sessions s
    JOIN events e ON s.session_id = e.session_id
    WHERE s.reached_payment = TRUE
    GROUP BY s.session_id, s.is_purchased
),
classified_payment_sessions AS (
    SELECT
        session_id,
        is_purchased,
        total_attempts,
        failure_count,
        distinct_methods_used,
        CASE
            WHEN failure_count = 0 AND is_purchased = TRUE THEN 'Clean Pass (No Failures)'
            WHEN failure_count = 0 AND is_purchased = FALSE THEN 'Pre-Attempt Dropout'
            WHEN failure_count > 0 AND is_purchased = TRUE AND distinct_methods_used = 1 THEN 'Recovered via Retry (Same Method)'
            WHEN failure_count > 0 AND is_purchased = TRUE AND distinct_methods_used > 1 THEN 'Recovered via Method Switch'
            WHEN failure_count > 0 AND is_purchased = FALSE THEN 'Abandoned Post-Failure'
            ELSE 'Other'
        END AS payment_journey_segment
    FROM session_payment_flow
)
SELECT
    payment_journey_segment,
    COUNT(*) AS session_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_of_payment_cohort_pct,
    ROUND(AVG(total_attempts), 2) AS avg_attempts_per_session,
    SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) AS completed_orders,
    ROUND(SUM(CASE WHEN is_purchased = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS recovery_conversion_rate_pct
FROM classified_payment_sessions
GROUP BY payment_journey_segment
ORDER BY session_count DESC;
