"""
ShopSphere Phase 4 Root-Cause & Interaction Analysis Engine
============================================================
Performs deep-dive statistical investigations, interaction modeling, threshold analysis,
and terminal state diagnosis across all journey friction points.
"""

import os
import duckdb
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

df_sessions = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "sessions.parquet"))
df_events = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "events.parquet"))
df_customers = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "customers.parquet"))
df_products = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "products.parquet"))

print("=" * 80)
print("  PHASE 4 ROOT-CAUSE & INTERACTION ANALYSIS")
print("=" * 80)

# ----------------------------------------------------------------------
# PART 2: ADDRESS ENTRY DEEP DIVE
# ----------------------------------------------------------------------
print("\n--- PART 2: Address Entry Deep Dive ---")
addr_sessions_ids = df_events[df_events['event_type'] == 'address_entry']['session_id'].unique()
ship_sessions_ids = df_events[df_events['event_type'] == 'shipping_view']['session_id'].unique()

df_addr = df_sessions[df_sessions['session_id'].isin(addr_sessions_ids)].copy()
df_addr['passed_address'] = df_addr['session_id'].isin(ship_sessions_ids).astype(int)

# Address pass rate by Device & Customer Type
addr_breakdown = df_addr.groupby(['device_type', 'customer_type']).agg(
    total_sessions=('session_id', 'count'),
    passed_sessions=('passed_address', 'sum'),
    mean_cart_val=('final_cart_value', 'mean'),
    median_duration=('session_duration_seconds', 'median')
).reset_index()
addr_breakdown['pass_rate_pct'] = (addr_breakdown['passed_sessions'] / addr_breakdown['total_sessions']) * 100
addr_breakdown['dropout_count'] = addr_breakdown['total_sessions'] - addr_breakdown['passed_sessions']
addr_breakdown['dropout_rate_pct'] = (addr_breakdown['dropout_count'] / addr_breakdown['total_sessions']) * 100
print("Address Completion by Device & Customer Type:")
print(addr_breakdown.to_string(index=False))

# Multivariate Logistic Regression with Interactions
logit_addr = smf.logit(
    "passed_address ~ C(device_type, Treatment('desktop')) * C(customer_type, Treatment('new')) + final_cart_value",
    data=df_addr
).fit(disp=False)
print("\nAddress Step Multivariate Regression (with Interaction):")
print(logit_addr.summary().tables[1])

# Mobile Address Dwell Times (Passed vs Abandoned)
addr_events_df = df_events[df_events['event_type'] == 'address_entry'][['session_id', 'device_type', 'time_since_previous_event']].copy()
addr_events_df['passed'] = addr_events_df['session_id'].isin(ship_sessions_ids)

mob_addr_events = addr_events_df[addr_events_df['device_type'] == 'mobile']
desk_addr_events = addr_events_df[addr_events_df['device_type'] == 'desktop']

print("\nAddress Dwell Time Summary:")
print(f"Mobile Address Dwell: Median = {mob_addr_events['time_since_previous_event'].median():.1f}s, IQR = {mob_addr_events['time_since_previous_event'].quantile(0.75)-mob_addr_events['time_since_previous_event'].quantile(0.25):.1f}s, Mean = {mob_addr_events['time_since_previous_event'].mean():.1f}s")
print(f"Desktop Address Dwell: Median = {desk_addr_events['time_since_previous_event'].median():.1f}s, IQR = {desk_addr_events['time_since_previous_event'].quantile(0.75)-desk_addr_events['time_since_previous_event'].quantile(0.25):.1f}s, Mean = {desk_addr_events['time_since_previous_event'].mean():.1f}s")

# ----------------------------------------------------------------------
# PART 3: SHIPPING COST & THRESHOLD ANALYSIS
# ----------------------------------------------------------------------
print("\n--- PART 3: Shipping Cost & Free Shipping Threshold Analysis ---")
ship_df = df_events[df_events['event_type'] == 'shipping_view'].copy()
sess_dropoff = df_sessions.set_index('session_id')['dropoff_stage']
ship_df['dropoff_stage'] = ship_df['session_id'].map(sess_dropoff)
ship_df['abandoned_at_shipping'] = (ship_df['dropoff_stage'] == 'shipping').astype(int)
ship_df['ship_ratio'] = ship_df['shipping_cost'] / ship_df['cart_value']
ship_df['is_free_shipping'] = (ship_df['shipping_cost'] == 0.0).astype(int)

# Behavior around $75 threshold
ship_df['cart_band'] = pd.cut(
    ship_df['cart_value'],
    bins=[0, 40, 60, 74.99, 75.00, 90, 120, 1000],
    labels=['<$40', '$40-$60', '$60-$74.99 (Near Threshold)', '$75 (Exact)', '$75-$90', '$90-$120', '>$120']
)

threshold_analysis = ship_df.groupby('cart_band', observed=True).agg(
    sessions=('session_id', 'count'),
    mean_shipping_cost=('shipping_cost', 'mean'),
    mean_ship_ratio=('ship_ratio', 'mean'),
    abandoned_shipping=('abandoned_at_shipping', 'sum'),
    free_shipping_share=('is_free_shipping', 'mean')
).reset_index()
threshold_analysis['shipping_dropoff_rate_pct'] = (threshold_analysis['abandoned_shipping'] / threshold_analysis['sessions']) * 100
threshold_analysis['free_shipping_share_pct'] = threshold_analysis['free_shipping_share'] * 100
print("Shipping Stage Attrition Across Cart Value Bands:")
print(threshold_analysis[['cart_band', 'sessions', 'mean_shipping_cost', 'mean_ship_ratio', 'free_shipping_share_pct', 'shipping_dropoff_rate_pct']].to_string(index=False))

# Backtracking Analysis near threshold ($60 - $74.99)
first_cs_df = df_events[df_events['event_type'] == 'checkout_start'].groupby('session_id')['event_sequence'].min()
events_with_cs = df_events.copy()
events_with_cs['first_cs_seq'] = events_with_cs['session_id'].map(first_cs_df)
backtrack_sess_ids = events_with_cs[(events_with_cs['event_sequence'] > events_with_cs['first_cs_seq']) &
                                    (events_with_cs['event_type'].isin(['cart_view', 'product_view']))]['session_id'].unique()

ship_df['is_backtrack'] = ship_df['session_id'].isin(backtrack_sess_ids)
backtrack_by_band = ship_df.groupby('cart_band', observed=True).agg(
    total_sessions=('session_id', 'count'),
    backtrack_sessions=('is_backtrack', 'sum')
).reset_index()
backtrack_by_band['backtrack_rate_pct'] = (backtrack_by_band['backtrack_sessions'] / backtrack_by_band['total_sessions']) * 100
print("\nBacktracking Frequency by Cart Band at Shipping View:")
print(backtrack_by_band.to_string(index=False))

# ----------------------------------------------------------------------
# PART 4: PAYMENT FAILURE & RECOVERY
# ----------------------------------------------------------------------
print("\n--- PART 4: Payment Failure & Gateway Diagnostics ---")
pay_events = df_events[df_events['event_type'].isin(['payment_success', 'payment_failed'])].copy()
pay_by_method = pay_events.groupby('payment_method').agg(
    total_attempts=('event_id', 'count'),
    successes=('event_type', lambda x: (x == 'payment_success').sum()),
    failures=('event_type', lambda x: (x == 'payment_failed').sum())
).reset_index()
pay_by_method['failure_rate_pct'] = (pay_by_method['failures'] / pay_by_method['total_attempts']) * 100
pay_by_method['auth_success_rate_pct'] = (pay_by_method['successes'] / pay_by_method['total_attempts']) * 100
print(pay_by_method.to_string(index=False))

# Session level payment transitions
pay_fail_sessions = df_events[df_events['event_type'] == 'payment_failed']['session_id'].unique()
purchased_sessions = df_sessions[df_sessions['is_purchased'] == True]['session_id'].unique()

recovered_sess = set(pay_fail_sessions).intersection(set(purchased_sessions))
unrecovered_sess = set(pay_fail_sessions) - set(purchased_sessions)

print(f"\nTotal Sessions encountering Payment Failure: {len(pay_fail_sessions):,}")
print(f"  Recovered to Completed Order: {len(recovered_sess):,} ({len(recovered_sess)/len(pay_fail_sessions)*100:.2f}%)")
print(f"  Unrecovered Abandonments:     {len(unrecovered_sess):,} ({len(unrecovered_sess)/len(pay_fail_sessions)*100:.2f}%)")

# ----------------------------------------------------------------------
# PART 5: PROMO CODE INVESTIGATION & SELECTION
# ----------------------------------------------------------------------
print("\n--- PART 5: Promo Code Investigation & Selection Profile ---")
cart_sess = df_sessions[df_sessions['reached_cart'] == True].copy()
valid_promo_ids = df_events[(df_events['event_type'] == 'promo_applied') & (df_events['error_code'].isnull())]['session_id'].unique()
invalid_promo_ids = df_events[df_events['error_code'] == 'ERR_INVALID_PROMO']['session_id'].unique()

cart_sess['promo_cohort'] = 'No Promo Attempted'
cart_sess.loc[cart_sess['session_id'].isin(valid_promo_ids), 'promo_cohort'] = 'Valid Promo Applied'
cart_sess.loc[cart_sess['session_id'].isin(invalid_promo_ids), 'promo_cohort'] = 'Invalid Promo Error'

promo_profile = cart_sess.groupby('promo_cohort').agg(
    sessions=('session_id', 'count'),
    mean_cart_value=('final_cart_value', 'mean'),
    median_cart_value=('final_cart_value', 'median'),
    mobile_share=('device_type', lambda x: (x == 'mobile').mean() * 100),
    new_cust_share=('customer_type', lambda x: (x == 'new').mean() * 100),
    checkout_rate=('reached_checkout', lambda x: x.mean() * 100),
    session_cvr=('is_purchased', lambda x: x.mean() * 100)
).reset_index()
print(promo_profile.to_string(index=False))

# ----------------------------------------------------------------------
# PART 8: SEGMENT INTERACTIONS
# ----------------------------------------------------------------------
print("\n--- PART 8: Key Segment Interactions ---")
# Interaction 1: Device x Cart Value at Address Entry
df_addr['cart_tier'] = pd.cut(df_addr['final_cart_value'], bins=[0, 60, 120, 1000], labels=['<$60', '$60-$120', '>$120'])
dev_cart_int = df_addr.groupby(['device_type', 'cart_tier'], observed=True).agg(
    sessions=('session_id', 'count'),
    pass_rate=('passed_address', lambda x: x.mean() * 100)
).reset_index()
print("Device x Cart Value at Address Entry:")
print(dev_cart_int.to_string(index=False))

# Interaction 2: Payment Method x Cart Value
checkout_succ = df_events[df_events['event_type'] == 'payment_attempt'].copy()
checkout_succ['cart_tier'] = pd.cut(checkout_succ['cart_value'], bins=[0, 75, 150, 1000], labels=['Low (<$75)', 'Med ($75-$150)', 'High (>$150)'])
pay_cart_int = checkout_succ.groupby(['payment_method', 'cart_tier'], observed=True).agg(
    attempts=('event_id', 'count'),
    declines=('error_code', lambda x: x.notnull().mean() * 100)
).reset_index()
print("\nPayment Method x Cart Tier Decline Rates (%):")
print(pay_cart_int.to_string(index=False))

# ----------------------------------------------------------------------
# PART 9: TERMINAL STATE DIAGNOSIS
# ----------------------------------------------------------------------
print("\n--- PART 9: Terminal Abandonment State Diagnosis ---")
term_diag = df_sessions.groupby('dropoff_stage').agg(
    session_count=('session_id', 'count'),
    mean_duration=('session_duration_seconds', 'mean'),
    median_duration=('session_duration_seconds', 'median'),
    mean_cart_val=('final_cart_value', 'mean'),
    mobile_share=('device_type', lambda x: (x == 'mobile').mean() * 100),
    new_share=('customer_type', lambda x: (x == 'new').mean() * 100)
).reset_index()

tot_sess = len(df_sessions)
tot_aban = len(df_sessions[df_sessions['dropoff_stage'] != 'converted'])

term_diag['traffic_share_pct'] = (term_diag['session_count'] / tot_sess) * 100
term_diag['abandon_share_pct'] = term_diag.apply(
    lambda r: (r['session_count'] / tot_aban * 100) if r['dropoff_stage'] != 'converted' else 0.0, axis=1
)

# Sort logically along the funnel
stage_order = {'browsing': 1, 'cart': 2, 'address': 3, 'shipping': 4, 'payment': 5, 'converted': 6}
term_diag['stage_order'] = term_diag['dropoff_stage'].map(stage_order)
term_diag = term_diag.sort_values('stage_order').drop(columns=['stage_order'])

print(term_diag.to_string(index=False))
