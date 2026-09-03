"""
ShopSphere Experiment Sample Size & Statistical Power Planning Engine (Phase 5)
================================================================================
Calculates sample size, MDE, statistical power, and duration estimates for candidate
A/B testing experiments using empirical baseline metrics from Phase 3 & 4.
"""

import os
import numpy as np
import pandas as pd
import scipy.stats as stats

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

df_sessions = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "sessions.parquet"))
df_events = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "events.parquet"))

print("=" * 80)
print("  PHASE 5 EXPERIMENT POWER & SAMPLE SIZE PLANNING")
print("=" * 80)

def calculate_sample_size(p1, mde_relative, alpha=0.05, power=0.80):
    """
    Standard two-sided two-sample proportion test sample size calculation per variant.
    """
    p2 = p1 * (1 + mde_relative)
    p_pooled = (p1 + p2) / 2

    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    numerator = (z_alpha * np.sqrt(2 * p_pooled * (1 - p_pooled)) + z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2

    n_per_variant = int(np.ceil(numerator / denominator))
    return n_per_variant, p2

# ----------------------------------------------------------------------
# 1. EXP-01: Mobile Address Form Autofill & Express Checkout
# ----------------------------------------------------------------------
# Eligible population: Mobile sessions reaching Address Entry
addr_sess_ids = df_events[df_events['event_type'] == 'address_entry']['session_id'].unique()
mob_addr_sess = df_sessions[(df_sessions['session_id'].isin(addr_sess_ids)) & (df_sessions['device_type'] == 'mobile')]
ship_sess_ids = df_events[df_events['event_type'] == 'shipping_view']['session_id'].unique()

mob_addr_base_cvr = (mob_addr_sess['session_id'].isin(ship_sess_ids)).mean() # 0.7918 (79.18%)
daily_mob_addr_traffic = len(mob_addr_sess) / 90.0 # ~147.1 sessions/day

# Planning MDE: +4.0% relative lift (~+3.17 pp to reach 82.35%)
n_exp01, p2_exp01 = calculate_sample_size(mob_addr_base_cvr, mde_relative=0.04, alpha=0.05, power=0.80)
total_n_exp01 = n_exp01 * 2
days_exp01 = total_n_exp01 / daily_mob_addr_traffic

print("\n--- EXP-01: Mobile Address Experience ---")
print(f"Eligible Traffic: Mobile Address Starters (90-day volume: {len(mob_addr_sess):,}, Daily: {daily_mob_addr_traffic:.1f}/day)")
print(f"Baseline Address Pass Rate (p1): {mob_addr_base_cvr*100:.2f}%")
print(f"Target Relative MDE: +4.0% (p2 = {p2_exp01*100:.2f}%)")
print(f"Sample Size per Variant (Alpha=0.05, Power=0.80): {n_exp01:,} sessions")
print(f"Total Experiment Sample Required: {total_n_exp01:,} sessions")
print(f"Estimated Runtime: {days_exp01:.1f} days (~{int(np.ceil(days_exp01/7))} weeks)")

# ----------------------------------------------------------------------
# 2. EXP-02: Dynamic Free Shipping Progress Bar & Proximity Messaging
# ----------------------------------------------------------------------
# Eligible population: Cart sessions with cart_value < $75
cart_sess = df_sessions[df_sessions['reached_cart'] == True].copy()
sub75_cart_sess = cart_sess[cart_sess['final_cart_value'] < 75.0]
sub75_purchased_rate = sub75_cart_sess['is_purchased'].mean() # Overall CVR from cart for sub-75
daily_sub75_cart_traffic = len(sub75_cart_sess) / 90.0 # ~148.4 sessions/day

# Planning MDE: +7.5% relative lift in cart-to-purchase conversion
n_exp02, p2_exp02 = calculate_sample_size(sub75_purchased_rate, mde_relative=0.075, alpha=0.05, power=0.80)
total_n_exp02 = n_exp02 * 2
days_exp02 = total_n_exp02 / daily_sub75_cart_traffic

print("\n--- EXP-02: Shipping Threshold Communication ---")
print(f"Eligible Traffic: Sub-$75 Cart Sessions (90-day volume: {len(sub75_cart_sess):,}, Daily: {daily_sub75_cart_traffic:.1f}/day)")
print(f"Baseline Cart-to-Purchase CVR (p1): {sub75_purchased_rate*100:.2f}%")
print(f"Target Relative MDE: +7.5% (p2 = {p2_exp02*100:.2f}%)")
print(f"Sample Size per Variant: {n_exp02:,} sessions")
print(f"Total Sample Required: {total_n_exp02:,} sessions")
print(f"Estimated Runtime: {days_exp02:.1f} days (~{int(np.ceil(days_exp02/7))} weeks)")

# ----------------------------------------------------------------------
# 3. EXP-03: Smart Payment Decline Recovery & Instant Alternative Fallback
# ----------------------------------------------------------------------
# Eligible population: Sessions encountering payment failure
pay_fail_sess_ids = df_events[df_events['event_type'] == 'payment_failed']['session_id'].unique()
pay_fail_sess = df_sessions[df_sessions['session_id'].isin(pay_fail_sess_ids)]
base_recovery_rate = pay_fail_sess['is_purchased'].mean() # 0.5228 (52.28%)
daily_fail_traffic = len(pay_fail_sess) / 90.0 # ~9.52 sessions/day

# Planning MDE: +15.0% relative lift in recovery rate (52.28% -> 60.12%)
n_exp03, p2_exp03 = calculate_sample_size(base_recovery_rate, mde_relative=0.15, alpha=0.05, power=0.80)
total_n_exp03 = n_exp03 * 2
days_exp03 = total_n_exp03 / daily_fail_traffic

print("\n--- EXP-03: Payment Decline Recovery Flow ---")
print(f"Eligible Traffic: Sessions encountering payment failure (90-day volume: {len(pay_fail_sess):,}, Daily: {daily_fail_traffic:.1f}/day)")
print(f"Baseline Payment Recovery Rate (p1): {base_recovery_rate*100:.2f}%")
print(f"Target Relative MDE: +15.0% (p2 = {p2_exp03*100:.2f}%)")
print(f"Sample Size per Variant: {n_exp03:,} sessions")
print(f"Total Sample Required: {total_n_exp03:,} sessions")
print(f"Estimated Runtime: {days_exp03:.1f} days (~{int(np.ceil(days_exp03/7))} weeks)")

# ----------------------------------------------------------------------
# 4. EXP-04: Collapsible Promo Code Field & Inline Error Guidance
# ----------------------------------------------------------------------
# Eligible population: All Cart Sessions
all_cart_traffic = len(cart_sess) / 90.0 # ~359.5 sessions/day
base_cart_to_checkout = cart_sess['reached_checkout'].mean() # 0.6160 (61.60%)

# Planning MDE: +3.0% relative lift in cart-to-checkout rate (61.60% -> 63.45%)
n_exp04, p2_exp04 = calculate_sample_size(base_cart_to_checkout, mde_relative=0.03, alpha=0.05, power=0.80)
total_n_exp04 = n_exp04 * 2
days_exp04 = total_n_exp04 / all_cart_traffic

print("\n--- EXP-04: Promo Validation Experience ---")
print(f"Eligible Traffic: All Cart Sessions (90-day volume: {len(cart_sess):,}, Daily: {all_cart_traffic:.1f}/day)")
print(f"Baseline Cart-to-Checkout Rate (p1): {base_cart_to_checkout*100:.2f}%")
print(f"Target Relative MDE: +3.0% (p2 = {p2_exp04*100:.2f}%)")
print(f"Sample Size per Variant: {n_exp04:,} sessions")
print(f"Total Sample Required: {total_n_exp04:,} sessions")
print(f"Estimated Runtime: {days_exp04:.1f} days (~{int(np.ceil(days_exp04/7))} weeks)")

print("\n" + "=" * 80)
print("  POWER & DURATION PLANNING SUMMARY TABLE")
print("=" * 80)

summary_table = pd.DataFrame([
    {
        "Experiment ID": "EXP-01",
        "Name": "Mobile Address Autofill & Express Checkout",
        "Primary Metric": "Mobile Address Pass Rate",
        "Baseline": f"{mob_addr_base_cvr*100:.2f}%",
        "Target Relative MDE": "+4.0%",
        "Target Absolute Rate": f"{p2_exp01*100:.2f}%",
        "Sample / Arm": f"{n_exp01:,}",
        "Total Sample": f"{total_n_exp01:,}",
        "Daily Traffic": f"{daily_mob_addr_traffic:.1f}",
        "Est. Runtime": f"{days_exp01:.0f} days ({int(np.ceil(days_exp01/7))} wks)"
    },
    {
        "Experiment ID": "EXP-02",
        "Name": "Shipping Threshold Progress Bar",
        "Primary Metric": "Sub-$75 Cart-to-Purchase CVR",
        "Baseline": f"{sub75_purchased_rate*100:.2f}%",
        "Target Relative MDE": "+7.5%",
        "Target Absolute Rate": f"{p2_exp02*100:.2f}%",
        "Sample / Arm": f"{n_exp02:,}",
        "Total Sample": f"{total_n_exp02:,}",
        "Daily Traffic": f"{daily_sub75_cart_traffic:.1f}",
        "Est. Runtime": f"{days_exp02:.0f} days ({int(np.ceil(days_exp02/7))} wks)"
    },
    {
        "Experiment ID": "EXP-03",
        "Name": "Smart Payment Decline Recovery Flow",
        "Primary Metric": "Payment Failure Recovery Rate",
        "Baseline": f"{base_recovery_rate*100:.2f}%",
        "Target Relative MDE": "+15.0%",
        "Target Absolute Rate": f"{p2_exp03*100:.2f}%",
        "Sample / Arm": f"{n_exp03:,}",
        "Total Sample": f"{total_n_exp03:,}",
        "Daily Traffic": f"{daily_fail_traffic:.1f}",
        "Est. Runtime": f"{days_exp03:.0f} days ({int(np.ceil(days_exp03/7))} wks)"
    },
    {
        "Experiment ID": "EXP-04",
        "Name": "Collapsible Promo Field & Inline Guidance",
        "Primary Metric": "Cart-to-Checkout Initiation Rate",
        "Baseline": f"{base_cart_to_checkout*100:.2f}%",
        "Target Relative MDE": "+3.0%",
        "Target Absolute Rate": f"{p2_exp04*100:.2f}%",
        "Sample / Arm": f"{n_exp04:,}",
        "Total Sample": f"{total_n_exp04:,}",
        "Daily Traffic": f"{all_cart_traffic:.1f}",
        "Est. Runtime": f"{days_exp04:.0f} days ({int(np.ceil(days_exp04/7))} wks)"
    }
])

print(summary_table.to_string(index=False))
