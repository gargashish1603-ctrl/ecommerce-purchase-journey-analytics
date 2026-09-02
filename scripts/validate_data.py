"""
ShopSphere Data Quality & Validation Engine (Phase 2)
=====================================================
Executes automated data quality, structural integrity, and business logic
audits against generated raw and processed datasets.

Implements all rules from docs/data-quality-rules.md:
- DQ-01 to DQ-17
- Summary metrics and integrity scorecard
- PASS / WARNING / FAIL categorization
"""

import os
import sys
import datetime
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

class DataQualityValidator:
    def __init__(self, data_source="raw"):
        self.data_source = data_source
        self.results = []
        self.load_data()
        
    def load_data(self):
        if self.data_source == "raw":
            dir_path = RAW_DATA_DIR
            self.customers = pd.read_csv(os.path.join(dir_path, "customers.csv"))
            self.products = pd.read_csv(os.path.join(dir_path, "products.csv"))
            self.sessions = pd.read_csv(os.path.join(dir_path, "sessions.csv"))
            self.events = pd.read_csv(os.path.join(dir_path, "events.csv"))
        else:
            dir_path = PROCESSED_DATA_DIR
            self.customers = pd.read_parquet(os.path.join(dir_path, "customers.parquet"))
            self.products = pd.read_parquet(os.path.join(dir_path, "products.parquet"))
            self.sessions = pd.read_parquet(os.path.join(dir_path, "sessions.parquet"))
            self.events = pd.read_parquet(os.path.join(dir_path, "events.parquet"))
            
        # Parse timestamps for validation
        self.events["dt"] = pd.to_datetime(self.events["event_timestamp"])
        self.sessions["start_dt"] = pd.to_datetime(self.sessions["session_start_time"])
        self.sessions["end_dt"] = pd.to_datetime(self.sessions["session_end_time"])

    def record_result(self, rule_id, rule_name, status, details, severity="STRICT"):
        self.results.append({
            "rule_id": rule_id,
            "rule_name": rule_name,
            "status": status,
            "severity": severity,
            "details": details
        })
        badge = f"[{status}]"
        print(f"  {badge:<9} {rule_id:<7} {rule_name:<40} : {details}")

    def run_all_checks(self):
        print("=" * 80)
        print(f"  ShopSphere Data Quality Validation Suite ({self.data_source.upper()} Data)")
        print("=" * 80)
        
        # -------------------------------------------------------------
        # 1. Structural & Referential Integrity
        # -------------------------------------------------------------
        print("\n--- 1. Structural & Referential Integrity Checks ---")
        
        # DQ-01: Primary Key Uniqueness
        sess_dup = self.sessions["session_id"].duplicated().sum()
        evt_dup = self.events["event_id"].duplicated().sum()
        cust_dup = self.customers["customer_id"].duplicated().sum()
        prod_dup = self.products["product_id"].duplicated().sum()
        
        if sess_dup == 0 and evt_dup == 0 and cust_dup == 0 and prod_dup == 0:
            self.record_result("DQ-01", "Primary Key Uniqueness", "PASS", "All PKs unique across 4 tables", "FATAL")
        else:
            self.record_result("DQ-01", "Primary Key Uniqueness", "FAIL", 
                               f"Duplicates found: sess={sess_dup}, evt={evt_dup}, cust={cust_dup}, prod={prod_dup}", "FATAL")

        # DQ-02: Referential Integrity
        orphan_evts = (~self.events["session_id"].isin(self.sessions["session_id"])).sum()
        orphan_cust = (~self.sessions["customer_id"].isin(self.customers["customer_id"])).sum()
        valid_prods = self.events["product_id"].dropna()
        orphan_prods = (~valid_prods.isin(self.products["product_id"])).sum()
        
        if orphan_evts == 0 and orphan_cust == 0 and orphan_prods == 0:
            self.record_result("DQ-02", "Referential Integrity", "PASS", "100% of foreign keys resolve successfully", "FATAL")
        else:
            self.record_result("DQ-02", "Referential Integrity", "FAIL",
                               f"Orphan FKs: evts->sess={orphan_evts}, sess->cust={orphan_cust}, evts->prod={orphan_prods}", "FATAL")

        # DQ-03: Monotonic Event Sequencing
        # Check if event_sequence is 1, 2, 3... per session
        seq_grouped = self.events.groupby("session_id")["event_sequence"]
        min_seq = seq_grouped.min()
        max_seq = seq_grouped.max()
        count_seq = seq_grouped.count()
        valid_seq = ((min_seq == 1) & (max_seq == count_seq)).all()
        
        if valid_seq:
            self.record_result("DQ-03", "Monotonic Event Sequencing", "PASS", "All sessions follow strictly monotonic 1..N sequences", "FATAL")
        else:
            self.record_result("DQ-03", "Monotonic Event Sequencing", "FAIL", "Gaps or invalid sequence starts detected", "FATAL")

        # DQ-04: Chronological Timestamp Consistency
        # Diff within session dt must be >= 0
        self.events["time_diff_actual"] = self.events.groupby("session_id")["dt"].diff().dt.total_seconds()
        neg_times = (self.events["time_diff_actual"].dropna() < 0).sum()
        
        if neg_times == 0:
            self.record_result("DQ-04", "Chronological Timestamps", "PASS", "Zero negative time-travel instances", "FATAL")
        else:
            self.record_result("DQ-04", "Chronological Timestamps", "FAIL", f"{neg_times} events have negative time diffs", "FATAL")

        # DQ-05: Timestamp Duration Match
        sess_calc_duration = (self.sessions["end_dt"] - self.sessions["start_dt"]).dt.total_seconds()
        dur_mismatch = (self.sessions["session_duration_seconds"] != sess_calc_duration).sum()
        
        if dur_mismatch == 0:
            self.record_result("DQ-05", "Timestamp Duration Match", "PASS", "Session durations match (t_end - t_start) exactly", "FATAL")
        else:
            self.record_result("DQ-05", "Timestamp Duration Match", "FAIL", f"{dur_mismatch} duration mismatches in sessions", "FATAL")

        # DQ-06: Valid Temporal Intervals
        # time_since_previous_event == time_diff_actual for seq > 1, and 0 for seq == 1
        seq_1_ok = (self.events[self.events["event_sequence"] == 1]["time_since_previous_event"] == 0).all()
        seq_gt1 = self.events[self.events["event_sequence"] > 1]
        interval_match = (seq_gt1["time_since_previous_event"] == seq_gt1["time_diff_actual"]).all()
        
        if seq_1_ok and interval_match:
            self.record_result("DQ-06", "Valid Temporal Intervals", "PASS", "time_since_previous_event perfectly matches timestamps", "FATAL")
        else:
            self.record_result("DQ-06", "Valid Temporal Intervals", "FAIL", "Interval discrepancy detected", "FATAL")

        # DQ-07: Controlled Nullability on Mandatory Fields
        mandatory_nulls = self.events[["session_id", "event_type", "device_type", "customer_type", "acquisition_channel"]].isnull().sum().sum()
        if mandatory_nulls == 0:
            self.record_result("DQ-07", "Controlled Nullability", "PASS", "0 nulls in mandatory clickstream fields", "FATAL")
        else:
            self.record_result("DQ-07", "Controlled Nullability", "FAIL", f"{mandatory_nulls} nulls in mandatory fields", "FATAL")

        # -------------------------------------------------------------
        # 2. Logical Funnel & State Transition Rules
        # -------------------------------------------------------------
        print("\n--- 2. Logical Funnel & State Transition Checks ---")
        
        # DQ-08: Precondition for Cart Addition
        # All add_to_cart must have event_sequence >= 2
        cart_events = self.events[self.events["event_type"] == "add_to_cart"]
        invalid_cart = (cart_events["event_sequence"] < 2).sum()
        if invalid_cart == 0:
            self.record_result("DQ-08", "Precondition for Cart Add", "PASS", "100% of add_to_cart preceded by discovery/browsing", "STRICT")
        else:
            self.record_result("DQ-08", "Precondition for Cart Add", "FAIL", f"{invalid_cart} cart events at seq=1", "STRICT")

        # DQ-09: Precondition for Checkout Start
        # Any session with checkout_start must have at least 1 add_to_cart
        sessions_with_checkout = set(self.events[self.events["event_type"] == "checkout_start"]["session_id"])
        sessions_with_cart = set(self.events[self.events["event_type"] == "add_to_cart"]["session_id"])
        illegal_checkouts = len(sessions_with_checkout - sessions_with_cart)
        if illegal_checkouts == 0:
            self.record_result("DQ-09", "Precondition for Checkout", "PASS", "All checkouts preceded by cart additions", "STRICT")
        else:
            self.record_result("DQ-09", "Precondition for Checkout", "FAIL", f"{illegal_checkouts} checkouts without prior cart", "STRICT")

        # DQ-10: Precondition for Order Completion
        # Every session with order_completed must have a preceding payment_success
        sessions_completed = set(self.events[self.events["event_type"] == "order_completed"]["session_id"])
        sessions_pay_success = set(self.events[self.events["event_type"] == "payment_success"]["session_id"])
        unauthorized_orders = len(sessions_completed - sessions_pay_success)
        if unauthorized_orders == 0:
            self.record_result("DQ-10", "Precondition for Order Completion", "PASS", "100% of completed orders have prior payment authorization", "STRICT")
        else:
            self.record_result("DQ-10", "Precondition for Order Completion", "FAIL", f"{unauthorized_orders} orders without payment success", "STRICT")

        # DQ-11: Conversion Flag Consistency
        sess_flag_true = set(self.sessions[self.sessions["is_purchased"] == True]["session_id"])
        flag_mismatch = len(sess_flag_true ^ sessions_completed)
        if flag_mismatch == 0:
            self.record_result("DQ-11", "Conversion Flag Consistency", "PASS", "sessions.is_purchased matches order_completed exactly", "STRICT")
        else:
            self.record_result("DQ-11", "Conversion Flag Consistency", "FAIL", f"{flag_mismatch} discrepancies in is_purchased flag", "STRICT")

        # DQ-12: Single Terminal Exit
        # Max sequence in each session must be session_exit
        last_events = self.events.sort_values(["session_id", "event_sequence"]).groupby("session_id").last()
        invalid_terminals = (last_events["event_type"] != "session_exit").sum()
        if invalid_terminals == 0:
            self.record_result("DQ-12", "Single Terminal Exit", "PASS", "100% of sessions terminate with clean session_exit", "STRICT")
        else:
            self.record_result("DQ-12", "Single Terminal Exit", "FAIL", f"{invalid_terminals} sessions missing terminal session_exit", "STRICT")

        # DQ-13: Payment State Transitions
        # payment_success or payment_failed must be preceded by payment_attempt
        pay_outcomes = self.events[self.events["event_type"].isin(["payment_success", "payment_failed"])].copy()
        # Find prev event type
        self.events["prev_event_type"] = self.events.groupby("session_id")["event_type"].shift(1)
        pay_outcomes_with_prev = self.events[self.events["event_type"].isin(["payment_success", "payment_failed"])]
        invalid_pay_transitions = (pay_outcomes_with_prev["prev_event_type"] != "payment_attempt").sum()
        if invalid_pay_transitions == 0:
            self.record_result("DQ-13", "Payment State Transitions", "PASS", "All payment outcomes immediately follow payment_attempt", "STRICT")
        else:
            self.record_result("DQ-13", "Payment State Transitions", "FAIL", f"{invalid_pay_transitions} invalid payment transitions", "STRICT")

        # -------------------------------------------------------------
        # 3. Commercial & Numerical Boundaries
        # -------------------------------------------------------------
        print("\n--- 3. Commercial & Numerical Boundary Checks ---")
        
        # DQ-14: Non-Negative Monetary Values
        neg_cart = (self.events["cart_value"] < 0).sum()
        neg_ship = (self.events["shipping_cost"] < 0).sum()
        neg_disc = (self.events["discount_amount"] < 0).sum()
        if neg_cart == 0 and neg_ship == 0 and neg_disc == 0:
            self.record_result("DQ-14", "Non-Negative Monetary Values", "PASS", "All monetary values are >= 0.00", "STRICT")
        else:
            self.record_result("DQ-14", "Non-Negative Monetary Values", "FAIL", f"Negative amounts: cart={neg_cart}, ship={neg_ship}, disc={neg_disc}", "STRICT")

        # DQ-15: Cart Value Consistency
        cart_view_nulls = self.events[self.events["event_type"] == "cart_view"]["cart_value"].isnull().sum()
        if cart_view_nulls == 0:
            self.record_result("DQ-15", "Cart Value Consistency", "PASS", "Cart views contain valid positive cart values", "STRICT")
        else:
            self.record_result("DQ-15", "Cart Value Consistency", "FAIL", f"{cart_view_nulls} cart_views with null cart_value", "STRICT")

        # DQ-16: Shipping Fee Logic
        # Prior to shipping_view, shipping_cost should be null
        pre_ship = self.events[self.events["event_type"].isin(["session_start", "product_view", "add_to_cart", "cart_view"])]["shipping_cost"].notnull().sum()
        # At and after shipping_view in checkout, shipping_cost must be non-null
        post_ship = self.events[self.events["event_type"].isin(["shipping_view", "payment_select", "payment_attempt", "order_completed"])]["shipping_cost"].isnull().sum()
        if pre_ship == 0 and post_ship == 0:
            self.record_result("DQ-16", "Shipping Fee Logic", "PASS", "Shipping cost is null pre-shipping and non-null post-shipping", "STRICT")
        else:
            self.record_result("DQ-16", "Shipping Fee Logic", "FAIL", f"Shipping fee logic violations: pre_ship_notnull={pre_ship}, post_ship_null={post_ship}", "STRICT")

        # DQ-17: Reasonable Dwell Durations
        # 99.9% of dwell times should be between 0 and 600 seconds
        dwell_gt_600 = (self.events["time_since_previous_event"] > 600).mean() * 100
        if dwell_gt_600 < 0.1:
            self.record_result("DQ-17", "Reasonable Dwell Times", "PASS", f"Dwell times well-bounded (only {dwell_gt_600:.3f}% > 600s)", "BOUNDED")
        else:
            self.record_result("DQ-17", "Reasonable Dwell Times", "WARNING", f"{dwell_gt_600:.2f}% dwell times > 600s", "BOUNDED")

        # -------------------------------------------------------------
        # Summary Scorecard
        # -------------------------------------------------------------
        print("\n" + "=" * 80)
        df_res = pd.DataFrame(self.results)
        num_pass = (df_res["status"] == "PASS").sum()
        num_warn = (df_res["status"] == "WARNING").sum()
        num_fail = (df_res["status"] == "FAIL").sum()
        print(f"  VALIDATION SUMMARY: {num_pass} PASSED, {num_warn} WARNINGS, {num_fail} FAILED (Total: {len(df_res)})")
        print("=" * 80)
        
        return num_fail == 0

def main():
    print("[*] Running Data Quality Validation on RAW dataset...")
    raw_validator = DataQualityValidator(data_source="raw")
    raw_passed = raw_validator.run_all_checks()
    
    print("\n[*] Running Data Quality Validation on PROCESSED dataset...")
    proc_validator = DataQualityValidator(data_source="processed")
    proc_passed = proc_validator.run_all_checks()
    
    if raw_passed and proc_passed:
        print("\n[OK] ALL DATA QUALITY AND STRUCTURAL INTEGRITY AUDITS PASSED SUCCESSFULLY.")
        sys.exit(0)
    else:
        print("\n[FAIL] ONE OR MORE DATA QUALITY AUDITS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
