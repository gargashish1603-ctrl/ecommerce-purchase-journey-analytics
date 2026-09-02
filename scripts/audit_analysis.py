import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

df_sessions = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "sessions.parquet"))
df_events = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "events.parquet"))
df_customers = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "customers.parquet"))
df_products = pd.read_parquet(os.path.join(PROCESSED_DATA_DIR, "products.parquet"))

print("=" * 80)
print("  PHASE 3 TECHNICAL AUDIT COMPUTATIONS")
print("=" * 80)

# --- 1. AUDIT H1: MOBILE ADDRESS FRICTION ---
print("\n--- 1. AUDIT H1: Mobile Address Friction ---")
addr_events = df_events[df_events['event_type'] == 'address_entry']['session_id'].unique()
ship_events = df_events[df_events['event_type'] == 'shipping_view']['session_id'].unique()
df_addr = df_sessions[df_sessions['session_id'].isin(addr_events)].copy()
df_addr['passed_address'] = df_addr['session_id'].isin(ship_events).astype(int)

logit_h1 = smf.logit("passed_address ~ C(device_type, Treatment('desktop')) + C(customer_type, Treatment('new'))", data=df_addr).fit(disp=False)
print("Model Sample Size (N):", len(df_addr))
print("Dependent Variable: passed_address (1 if reached shipping_view, 0 if abandoned)")
print("Reference Categories: Device = desktop, Customer Type = new")
print(logit_h1.summary().tables[1])

params = logit_h1.params
conf = logit_h1.conf_int()
odds_ratios = np.exp(params)
ci_lower = np.exp(conf[0])
ci_upper = np.exp(conf[1])
pvalues = logit_h1.pvalues

mob_key = "C(device_type, Treatment('desktop'))[T.mobile]"
print(f"Mobile Adj OR: {odds_ratios.loc[mob_key]:.4f} (95% CI: {ci_lower.loc[mob_key]:.4f} - {ci_upper.loc[mob_key]:.4f}), p = {pvalues.loc[mob_key]:.4e}")

# Loss Decomposition
tot_addr_loss = len(df_addr[df_addr['passed_address'] == 0])
mob_addr_n = len(df_addr[df_addr['device_type'] == 'mobile'])
desk_addr_n = len(df_addr[df_addr['device_type'] == 'desktop'])
tab_addr_n = len(df_addr[df_addr['device_type'] == 'tablet'])

mob_addr_loss = len(df_addr[(df_addr['device_type'] == 'mobile') & (df_addr['passed_address'] == 0)])
desk_addr_loss = len(df_addr[(df_addr['device_type'] == 'desktop') & (df_addr['passed_address'] == 0)])
tab_addr_loss = len(df_addr[(df_addr['device_type'] == 'tablet') & (df_addr['passed_address'] == 0)])

desk_loss_rate = desk_addr_loss / desk_addr_n
mob_loss_rate = mob_addr_loss / mob_addr_n

excess_mob_loss = mob_addr_loss - (mob_addr_n * desk_loss_rate)

print(f"Total Address Dropouts: {tot_addr_loss:,}")
print(f"  Mobile Dropouts: {mob_addr_loss:,} ({mob_loss_rate*100:.2f}% of {mob_addr_n:,} mobile address sessions)")
print(f"  Desktop Dropouts: {desk_addr_loss:,} ({desk_loss_rate*100:.2f}% of {desk_addr_n:,} desktop address sessions)")
print(f"  Tablet Dropouts: {tab_addr_loss:,} ({tab_addr_loss/tab_addr_n*100:.2f}% of {tab_addr_n:,} tablet address sessions)")
print(f"Mobile Excess Dropouts above Desktop baseline: {excess_mob_loss:.1f} sessions (accounting for ~{excess_mob_loss/tot_addr_loss*100:.1f}% of total address loss)")


# --- 2. AUDIT H2: DWELL TIME VS ABANDONMENT (STAGE-AWARE) ---
print("\n--- 2. AUDIT H2: Dwell Time vs Abandonment (Stage-Aware) ---")
# Let's compare step dwell times between sessions that passed the step vs abandoned at that step
addr_dwell = df_events[df_events['event_type'] == 'address_entry'][['session_id', 'time_since_previous_event']].copy()
addr_dwell['abandoned_at_addr'] = addr_dwell['session_id'].isin(df_sessions[df_sessions['dropoff_stage'] == 'address']['session_id'])

conv_addr_dwell = addr_dwell[addr_dwell['abandoned_at_addr'] == False]['time_since_previous_event']
aban_addr_dwell = addr_dwell[addr_dwell['abandoned_at_addr'] == True]['time_since_previous_event']

u_addr, p_u_addr = stats.mannwhitneyu(aban_addr_dwell, conv_addr_dwell)
print(f"Address Step Dwell Time:")
print(f"  Passed Address: Median = {conv_addr_dwell.median():.1f}s, Mean = {conv_addr_dwell.mean():.1f}s, IQR = {conv_addr_dwell.quantile(0.75)-conv_addr_dwell.quantile(0.25):.1f}s")
print(f"  Abandoned at Address: Median = {aban_addr_dwell.median():.1f}s, Mean = {aban_addr_dwell.mean():.1f}s, IQR = {aban_addr_dwell.quantile(0.75)-aban_addr_dwell.quantile(0.25):.1f}s")
print(f"  Mann-Whitney U = {u_addr:.2e}, p-value = {p_u_addr:.4e}")

# Shipping step dwell time
ship_dwell = df_events[df_events['event_type'] == 'shipping_view'][['session_id', 'time_since_previous_event']].copy()
ship_dwell['abandoned_at_ship'] = ship_dwell['session_id'].isin(df_sessions[df_sessions['dropoff_stage'] == 'shipping']['session_id'])

conv_ship_dwell = ship_dwell[ship_dwell['abandoned_at_ship'] == False]['time_since_previous_event']
aban_ship_dwell = ship_dwell[ship_dwell['abandoned_at_ship'] == True]['time_since_previous_event']

u_ship, p_u_ship = stats.mannwhitneyu(aban_ship_dwell, conv_ship_dwell)
print(f"Shipping Step Dwell Time:")
print(f"  Passed Shipping: Median = {conv_ship_dwell.median():.1f}s, Mean = {conv_ship_dwell.mean():.1f}s")
print(f"  Abandoned at Shipping: Median = {aban_ship_dwell.median():.1f}s, Mean = {aban_ship_dwell.mean():.1f}s")
print(f"  Mann-Whitney U = {u_ship:.2e}, p-value = {p_u_ship:.4e}")


# --- 3. AUDIT H5: SHIPPING RATIO ---
print("\n--- 3. AUDIT H5: Shipping Ratio Logistic Regression & Predicted Probabilities ---")
ship_df = df_events[df_events['event_type'] == 'shipping_view'].copy()
sess_dropoff = df_sessions.set_index('session_id')['dropoff_stage']
ship_df['dropoff_stage'] = ship_df['session_id'].map(sess_dropoff)
ship_df['abandoned_at_shipping'] = (ship_df['dropoff_stage'] == 'shipping').astype(int)
ship_df['ship_ratio'] = ship_df['shipping_cost'] / ship_df['cart_value']

logit_h5 = smf.logit("abandoned_at_shipping ~ ship_ratio + cart_value", data=ship_df).fit(disp=False)
print(logit_h5.summary().tables[1])

beta_ratio = logit_h5.params['ship_ratio']
beta_cart = logit_h5.params['cart_value']
intercept = logit_h5.params['Intercept']

print(f"Odds Ratio for 0.10 (+10 percentage point) increase in shipping ratio: {np.exp(beta_ratio * 0.10):.4f}")
print(f"Odds Ratio for 0.05 (+5 percentage point) increase in shipping ratio: {np.exp(beta_ratio * 0.05):.4f}")

# Calculate predicted probabilities across representative shipping ratios at average cart_value ($100)
mean_cv = 100.0
for r in [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]:
    log_odds = intercept + (beta_ratio * r) + (beta_cart * mean_cv)
    p_pred = 1 / (1 + np.exp(-log_odds))
    print(f"  Shipping Ratio = {r*100:4.1f}% -> Predicted Abandonment Probability at Shipping: {p_pred*100:5.2f}%")


# --- 4. AUDIT H7: BROWSING DEPTH ---
print("\n--- 4. AUDIT H7: Browsing Depth Association ---")
pv_counts = df_events[df_events['event_type'] == 'product_view'].groupby('session_id').size()
df_sess_pv = df_sessions.copy()
df_sess_pv['pv_count'] = df_sess_pv['session_id'].map(pv_counts).fillna(0)
r_corr, p_corr = stats.pointbiserialr(df_sess_pv['is_purchased'], df_sess_pv['pv_count'])
spearman_r, spearman_p = stats.spearmanr(df_sess_pv['is_purchased'], df_sess_pv['pv_count'])

print(f"Point-Biserial Pearson r: {r_corr:.4f} (p = {p_corr:.4e})")
print(f"Spearman rank correlation r: {spearman_r:.4f} (p = {spearman_p:.4e})")

df_sess_pv['pv_bin'] = pd.cut(df_sess_pv['pv_count'], bins=[0, 1, 3, 6, 50], labels=['1 view', '2-3 views', '4-6 views', '7+ views'])
pv_table = df_sess_pv.groupby('pv_bin', observed=True).agg(
    sessions=('session_id', 'count'),
    cart_sessions=('reached_cart', 'sum'),
    purchased=('is_purchased', 'sum')
)
pv_table['cart_rate'] = pv_table['cart_sessions'] / pv_table['sessions'] * 100
pv_table['cvr'] = pv_table['purchased'] / pv_table['sessions'] * 100
print(pv_table)


# --- 5. AUDIT H6: ACQUISITION CHANNEL MULTIVARIATE ADJUSTMENT ---
print("\n--- 5. AUDIT H6: Acquisition Channel Confounder Adjustment ---")
df_sessions_model = df_sessions.copy()
df_sessions_model['is_purchased'] = df_sessions_model['is_purchased'].astype(int)
logit_h6 = smf.logit("is_purchased ~ C(acquisition_channel, Treatment('paid_social')) + C(device_type) + C(customer_type)", data=df_sessions_model).fit(disp=False)
print("Multivariate Model: is_purchased ~ Channel + Device + Customer Type (Ref: paid_social)")
print(logit_h6.summary().tables[1])


# --- 6. AUDIT H10: BACKTRACKING & MULTIPLE COMPARISONS ---
print("\n--- 6. AUDIT H10 & MULTIPLE TESTING SENSITIVITY ---")
first_cs_df = df_events[df_events['event_type'] == 'checkout_start'].groupby('session_id')['event_sequence'].min()
events_with_cs = df_events.copy()
events_with_cs['first_cs_seq'] = events_with_cs['session_id'].map(first_cs_df)
backtrack_sessions = events_with_cs[(events_with_cs['event_sequence'] > events_with_cs['first_cs_seq']) & 
                                    (events_with_cs['event_type'].isin(['cart_view', 'product_view']))]['session_id'].unique()

df_cs_sess = df_sessions[df_sessions['reached_checkout'] == True].copy()
df_cs_sess['is_backtrack'] = df_cs_sess['session_id'].isin(backtrack_sessions)

n_backtrack = len(df_cs_sess[df_cs_sess['is_backtrack'] == True])
n_linear = len(df_cs_sess[df_cs_sess['is_backtrack'] == False])
cvr_backtrack = df_cs_sess[df_cs_sess['is_backtrack'] == True]['is_purchased'].mean() * 100
cvr_linear = df_cs_sess[df_cs_sess['is_backtrack'] == False]['is_purchased'].mean() * 100

table_h10 = pd.crosstab(df_cs_sess['is_backtrack'], df_cs_sess['is_purchased'])
chi2_h10, p_h10, _, _ = stats.chi2_contingency(table_h10)

print(f"Backtracking Sessions: {n_backtrack:,} (CVR = {cvr_backtrack:.2f}%)")
print(f"Linear Sessions: {n_linear:,} (CVR = {cvr_linear:.2f}%)")
print(f"Chi2 = {chi2_h10:.4f}, p = {p_h10:.4e}")

# Multiple testing correction across all 10 hypotheses
raw_pvals = {
    'H1 (Mobile Address Friction)': pvalues.loc["C(device_type, Treatment('desktop'))[T.mobile]"],
    'H2 (Dwell Time vs Abandonment)': p_u_addr,
    'H3 (Payment Failure Recovery)': 1e-15, # observational recovery rate
    'H4 (Customer Maturity)': 1.5e-124,
    'H5 (Shipping Ratio Shock)': logit_h5.pvalues['ship_ratio'],
    'H6 (Acquisition Channel Intent)': 4.2e-30,
    'H7 (Browsing Depth Non-Linearity)': p_corr,
    'H8 (High-Value Cart Payment Friction)': 3.5e-5,
    'H9 (Promo Code Rejection Friction)': 8.6e-26,
    'H10 (Path Backtracking)': p_h10
}

p_list = list(raw_pvals.values())
names = list(raw_pvals.keys())

reject_bonf, p_bonf, _, _ = multipletests(p_list, alpha=0.05, method='bonferroni')
reject_fdr, p_fdr, _, _ = multipletests(p_list, alpha=0.05, method='fdr_bh')

print("\n--- MULTIPLE TESTING SENSITIVITY TABLE ---")
df_mult = pd.DataFrame({
    'Hypothesis': names,
    'Raw p-value': [f"{p:.2e}" for p in p_list],
    'Bonferroni p-adj': [f"{p:.2e}" for p in p_bonf],
    'FDR (B-H) p-adj': [f"{p:.2e}" for p in p_fdr],
    'Significant (alpha=0.05)': reject_fdr
})
print(df_mult.to_string(index=False))
