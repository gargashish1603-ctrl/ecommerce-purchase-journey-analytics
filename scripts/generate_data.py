"""
ShopSphere Synthetic Data Generator (Phase 2)
==============================================
Generates a realistic, distribution-driven e-commerce clickstream and relational dataset
for the ShopSphere Purchase Journey Analytics case study.

Strictly adheres to:
- docs/data-model.md
- docs/data-generation-principles.md
- docs/customer-journey.md
- docs/data-quality-rules.md
- Fixed master seed (SEED = 42) for 100% reproducibility.
"""

import os
import sys
import uuid
import math
import random
import datetime
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Master random seed for complete reproducibility
MASTER_SEED = 42
random.seed(MASTER_SEED)
np.random.seed(MASTER_SEED)

# Output directory configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 1. Product Catalog Definition
# ----------------------------------------------------------------------
CATEGORIES = {
    "Electronics": {
        "price_range": (35.0, 650.0),
        "price_log_mu": 4.8,
        "price_log_sigma": 0.8,
        "weight_tiers": ["light", "medium", "heavy"],
        "weight_probs": [0.3, 0.5, 0.2],
        "product_templates": [
            "Wireless Noise-Cancelling Headphones", "Ultra HD Smart Action Camera",
            "Mechanical RGB Gaming Keyboard", "Ergonomic Bluetooth Mouse",
            "Portable Power Bank 20000mAh", "4K Ultra-Slim Monitor 27-inch",
            "Smart Home Security Camera", "Fast Wireless Charging Stand",
            "True Wireless Stereo Earbuds", "USB-C Multi-Port Hub Adapter",
            "Smart Fitness Tracker Watch", "Compact Bluetooth Speaker",
            "Dash Cam with Night Vision", "Mini Projector 1080p Support",
            "High-Speed External SSD 1TB"
        ]
    },
    "Fashion & Apparel": {
        "price_range": (15.0, 160.0),
        "price_log_mu": 3.7,
        "price_log_sigma": 0.6,
        "weight_tiers": ["light", "medium"],
        "weight_probs": [0.85, 0.15],
        "product_templates": [
            "Classic Slim-Fit Denim Jeans", "100% Organic Cotton Crewneck T-Shirt",
            "Waterproof Hooded Windbreaker", "Breathable Mesh Running Sneakers",
            "Premium Wool Blend Cardigan", "Casual Linen Long-Sleeve Shirt",
            "High-Waisted Yoga Leggings", "Vintage Leather Messenger Bag",
            "Thermal Fleece Winter Jacket", "Lightweight Slip-On Loafers",
            "Polarized UV400 Sunglasses", "Water-Resistant Everyday Backpack",
            "Formal Silk Necktie & Pocket Square", "Quick-Dry Athletic Shorts",
            "Merino Wool Beanie Hat"
        ]
    },
    "Home & Kitchen": {
        "price_range": (20.0, 240.0),
        "price_log_mu": 4.0,
        "price_log_sigma": 0.7,
        "weight_tiers": ["light", "medium", "heavy", "oversized"],
        "weight_probs": [0.2, 0.45, 0.25, 0.1],
        "product_templates": [
            "Stainless Steel French Press Coffee Maker", "Cast Iron Pre-Seasoned Skillet 12-inch",
            "Air Purifier with HEPA Filter", "Programmable Digital Slow Cooker",
            "Ultrasonic Cool Mist Humidifier", "Bamboo Cutting Board 3-Piece Set",
            "Memory Foam Orthopedic Bed Pillow", "Precision Digital Kitchen Food Scale",
            "Microfiber Bed Sheet 4-Piece Set", "Electric Glass Kettle with Auto-Shutoff",
            "Professional Chef Knife 8-inch", "Double-Walled Insulated Travel Mug",
            "Heavy-Duty Handheld Garment Steamer", "Aromatherapy Essential Oil Diffuser",
            "Non-Stick Ceramic Cookware Set"
        ]
    },
    "Beauty & Personal Care": {
        "price_range": (12.0, 95.0),
        "price_log_mu": 3.3,
        "price_log_sigma": 0.5,
        "weight_tiers": ["light"],
        "weight_probs": [1.0],
        "product_templates": [
            "Hydrating Hyaluronic Acid Facial Serum", "Organic Moroccan Argan Hair Oil",
            "Mineral Sunscreen SPF 50 Broad Spectrum", "Gentle Foaming Daily Cleanser",
            "Sonic Electric Toothbrush Rechargeable", "Nourishing Night Cream with Retinol",
            "Exfoliating Sea Salt Body Scrub", "Rosewater Facial Toner & Mist",
            "Beard Grooming Kit with Sandalwood Oil", "Charcoal Purifying Clay Mask",
            "Vitamin C Brightening Eye Cream", "Repairing Shea Butter Hand Salve"
        ]
    },
    "Sports & Fitness": {
        "price_range": (18.0, 290.0),
        "price_log_mu": 4.1,
        "price_log_sigma": 0.75,
        "weight_tiers": ["light", "medium", "heavy"],
        "weight_probs": [0.4, 0.4, 0.2],
        "product_templates": [
            "Adjustable Neoprene Dumbbell Set", "Non-Slip Eco-Friendly Yoga Mat",
            "High-Density Foam Muscle Roller", "Resistance Bands Set with Handles",
            "Insulated Stainless Steel Water Bottle 32oz", "Speed Jump Rope with Ball Bearings",
            "Hydration Running Vest Pack", "Tactical Folding Camping Knife",
            "Ultralight Inflatable Sleeping Pad", "Compact Trekking Poles Pair",
            "Cycling Helmet with Rear Safety Light", "Gym Duffle Bag with Shoe Compartment"
        ]
    },
    "Books & Stationery": {
        "price_range": (8.0, 48.0),
        "price_log_mu": 2.8,
        "price_log_sigma": 0.45,
        "weight_tiers": ["light", "medium"],
        "weight_probs": [0.8, 0.2],
        "product_templates": [
            "Hardcover Dot-Grid Bullet Journal", "Refillable Brass Fountain Pen",
            "Product Management & Strategy Handbook", "Data Analytics in Practice Hardcover",
            "Minimalist Wooden Desk Organizer", "Noise-Dampening Felt Desk Mat",
            "Architectural Mechanical Pencil Set", "Watercolor Painting Starter Set",
            "Weekly Productivity Desk Planner", "Ergonomic Reading Book Stand"
        ]
    }
}

def generate_products(total_products=180):
    """Generates synthetic product catalog table."""
    products = []
    prod_idx = 1
    
    # Calculate category product counts
    cat_names = list(CATEGORIES.keys())
    cat_weights = [0.25, 0.25, 0.20, 0.12, 0.10, 0.08]
    cat_counts = np.random.multinomial(total_products, cat_weights)
    
    for cat_name, count in zip(cat_names, cat_counts):
        cat_info = CATEGORIES[cat_name]
        templates = cat_info["product_templates"]
        
        for i in range(count):
            base_template = templates[i % len(templates)]
            variant_suffix = f" (Edition { (i // len(templates)) + 1 })" if i >= len(templates) else ""
            p_name = f"{base_template}{variant_suffix}"
            
            # Sample realistic log-normal price bounded by range
            raw_price = np.random.lognormal(cat_info["price_log_mu"], cat_info["price_log_sigma"])
            p_min, p_max = cat_info["price_range"]
            price = round(float(np.clip(raw_price, p_min, p_max)), 2)
            
            weight_tier = np.random.choice(cat_info["weight_tiers"], p=cat_info["weight_probs"])
            
            products.append({
                "product_id": f"PROD-{prod_idx:04d}",
                "product_name": p_name,
                "category": cat_name,
                "base_price": price,
                "shipping_weight_tier": weight_tier
            })
            prod_idx += 1
            
    df_products = pd.DataFrame(products)
    return df_products

# ----------------------------------------------------------------------
# 2. Customer Population Generation
# ----------------------------------------------------------------------
PAYMENT_METHODS = ["credit_card", "digital_wallet", "debit_card", "bnpl", "net_banking"]
PAYMENT_METHOD_PROBS = [0.38, 0.28, 0.16, 0.10, 0.08]

def generate_customers(num_customers=55000):
    """Generates synthetic customer dimension table."""
    customers = []
    
    # Start date 1 year prior to campaign
    start_history = datetime.datetime(2025, 6, 1, 0, 0, 0)
    end_history = datetime.datetime(2026, 6, 1, 0, 0, 0)
    history_span_seconds = int((end_history - start_history).total_seconds())
    
    # Customer type split: ~60% new visitors, ~40% returning customers in master population
    customer_types = np.random.choice(["new", "returning"], size=num_customers, p=[0.60, 0.40])
    
    for i in range(num_customers):
        cust_id = f"CUST-{i+1:06d}"
        c_type = customer_types[i]
        
        if c_type == "returning":
            offset = np.random.randint(0, history_span_seconds)
            created_at = start_history + datetime.timedelta(seconds=offset)
            # Returning users have 1 to 12 lifetime orders
            lifetime_orders = int(np.random.geometric(p=0.3))
            pref_payment = np.random.choice(PAYMENT_METHODS, p=PAYMENT_METHOD_PROBS)
        else:
            # New customers: 70% pure guest (no account), 30% create account during period
            if np.random.random() < 0.30:
                offset = np.random.randint(0, history_span_seconds)
                created_at = start_history + datetime.timedelta(seconds=offset)
            else:
                created_at = None
            lifetime_orders = 0
            pref_payment = None
            
        customers.append({
            "customer_id": cust_id,
            "customer_type": c_type,
            "account_created_at": created_at.isoformat() if created_at else None,
            "lifetime_orders": lifetime_orders,
            "default_payment_preference": pref_payment
        })
        
    df_customers = pd.DataFrame(customers)
    return df_customers

# ----------------------------------------------------------------------
# 3. Session & Event Clickstream Simulation
# ----------------------------------------------------------------------
CHANNELS = ["organic_search", "paid_search", "paid_social", "direct", "email_crm", "affiliate"]
CHANNEL_PROBS = [0.26, 0.23, 0.24, 0.13, 0.08, 0.06]

DEVICES = ["mobile", "desktop", "tablet"]
DEVICE_PROBS = [0.63, 0.33, 0.04]

BROWSERS_BY_DEVICE = {
    "mobile": (["Chrome Mobile", "Safari Mobile", "Samsung Internet"], [0.55, 0.40, 0.05]),
    "desktop": (["Chrome", "Edge", "Safari", "Firefox"], [0.65, 0.18, 0.10, 0.07]),
    "tablet": (["Safari Mobile", "Chrome Mobile"], [0.70, 0.30])
}

DISCOUNT_CODES = {
    "WELCOME10": {"amount_type": "pct", "val": 0.10, "valid": True},
    "SPHERE20": {"amount_type": "pct", "val": 0.20, "valid": True},
    "FREESHIP": {"amount_type": "fixed_shipping", "val": 0.0, "valid": True},
    "EXPIRED50": {"amount_type": "pct", "val": 0.50, "valid": False},
    "DEAL100": {"amount_type": "fixed", "val": 100.0, "valid": False}
}

PAYMENT_ERRORS = [
    ("ERR_INSUFFICIENT_FUNDS", "Card decline: Insufficient available balance"),
    ("ERR_GATEWAY_TIMEOUT", "Payment gateway connection timeout"),
    ("ERR_3DS_AUTH_FAILED", "3D-Secure two-factor authentication failed"),
    ("ERR_CARD_EXPIRED", "Card expiration date is invalid or past"),
    ("ERR_BANK_DECLINE", "Transaction declined by issuing bank risk algorithm")
]

SHIPPING_BASE_RATES = {
    "light": 5.99,
    "medium": 8.99,
    "heavy": 14.99,
    "oversized": 24.99
}
FREE_SHIPPING_THRESHOLD = 75.0

def sample_dwell_time(stage, device_type):
    """Samples realistic human interaction dwell time in seconds using log-normal distribution."""
    # Base parameters (mu, sigma)
    params = {
        "session_start": (1.2, 0.4),       # ~3-5s
        "product_view": (3.1, 0.65),       # ~20-35s
        "add_to_cart": (1.8, 0.45),        # ~6-10s
        "cart_view": (2.7, 0.55),          # ~15-20s
        "promo_applied": (2.2, 0.50),      # ~8-12s
        "checkout_start": (2.3, 0.45),     # ~10-15s
        "address_entry": (3.6, 0.55),      # ~35-50s
        "shipping_view": (2.6, 0.50),      # ~12-18s
        "payment_select": (2.7, 0.50),     # ~14-20s
        "payment_attempt": (2.4, 0.40),    # ~10-15s (processing + submission)
        "payment_failed": (2.0, 0.40),     # ~7-10s
        "payment_success": (1.5, 0.35),    # ~4-6s
        "order_completed": (3.0, 0.50),    # ~20s review
        "session_exit": (0.8, 0.30)        # ~2s
    }
    mu, sigma = params.get(stage, (2.5, 0.5))
    
    # Slight device input adjustment: mobile form entry has slightly higher latency
    if stage == "address_entry" and device_type == "mobile":
        mu += 0.20
    elif stage == "payment_select" and device_type == "mobile":
        mu += 0.10
        
    sec = float(np.random.lognormal(mu, sigma))
    return max(1, min(int(round(sec)), 480))

def simulate_event_stream(num_sessions=100000, df_customers=None, df_products=None):
    """
    Generates realistic session clickstream events and builds corresponding sessions table.
    """
    print(f"[*] Simulating {num_sessions:,} customer sessions and event streams...")
    
    # Pre-index products by ID and popularity
    product_records = df_products.to_dict("records")
    num_prods = len(product_records)
    # Zipfian product popularity distribution
    zipf_weights = 1.0 / (np.arange(1, num_prods + 1) ** 0.8)
    zipf_probs = zipf_weights / zipf_weights.sum()
    
    # Customer pool
    cust_records = df_customers.to_dict("records")
    new_cust_pool = [c for c in cust_records if c["customer_type"] == "new"]
    ret_cust_pool = [c for c in cust_records if c["customer_type"] == "returning"]
    
    # Temporal window: 90 days from 2026-06-01 to 2026-08-30
    campaign_start = datetime.datetime(2026, 6, 1, 0, 0, 0)
    total_seconds_window = 90 * 24 * 3600
    
    all_events = []
    all_sessions = []
    
    # Event UUID generator counter for performance
    event_counter = 1
    
    for s_idx in range(1, num_sessions + 1):
        if s_idx % 25000 == 0:
            print(f"    -> Progress: {s_idx:,} / {num_sessions:,} sessions generated...")
            
        session_id = f"SESS-{s_idx:07d}"
        
        # 1. Determine Customer
        is_returning_session = (np.random.random() < 0.38)
        if is_returning_session and len(ret_cust_pool) > 0:
            cust = ret_cust_pool[np.random.randint(0, len(ret_cust_pool))]
            cust_type = "returning"
        else:
            cust = new_cust_pool[np.random.randint(0, len(new_cust_pool))]
            cust_type = "new"
            
        cust_id = cust["customer_id"]
        
        # 2. Acquisition Channel & Device
        # Channel assignment has slight customer type variation (returning has higher Direct/CRM)
        if cust_type == "returning":
            ch_probs = [0.18, 0.15, 0.12, 0.28, 0.22, 0.05]
        else:
            ch_probs = [0.28, 0.26, 0.30, 0.06, 0.02, 0.08]
        acq_channel = np.random.choice(CHANNELS, p=ch_probs)
        
        # Device assignment: Paid social leans more mobile
        if acq_channel == "paid_social":
            dev_probs = [0.78, 0.19, 0.03]
        else:
            dev_probs = DEVICE_PROBS
        device_type = np.random.choice(DEVICES, p=dev_probs)
        
        browser_list, b_probs = BROWSERS_BY_DEVICE[device_type]
        browser = np.random.choice(browser_list, p=b_probs)
        
        # 3. Session Start Timestamp with realistic diurnal & day-of-week curve
        day_offset = np.random.randint(0, 90)
        # Hour of day: peak at 18-22, trough at 2-5
        hour_weights = np.array([
            0.015, 0.010, 0.008, 0.006, 0.007, 0.012,
            0.025, 0.040, 0.055, 0.060, 0.058, 0.055,
            0.052, 0.050, 0.052, 0.056, 0.062, 0.075,
            0.085, 0.095, 0.090, 0.075, 0.052, 0.035
        ])
        hour_weights = hour_weights / hour_weights.sum()
        hour = np.random.choice(np.arange(24), p=hour_weights)
        minute = np.random.randint(0, 60)
        second = np.random.randint(0, 60)
        curr_time = campaign_start + datetime.timedelta(days=day_offset, hours=int(hour), minutes=int(minute), seconds=int(second))
        session_start_time = curr_time
        
        # 4. State Machine Execution
        seq = 1
        cart_items = []
        cart_value = 0.0
        shipping_cost = None
        discount_code = None
        discount_amount = 0.0
        active_payment_method = None
        dropoff_stage = "browsing"
        is_purchased = False
        
        # Helper to record event
        def add_event(e_type, p_id=None, p_cat=None, p_method=None, err_code=None, err_msg=None, interval=None):
            nonlocal seq, curr_time, event_counter
            if interval is None:
                interval = sample_dwell_time(e_type, device_type) if seq > 1 else 0
            curr_time += datetime.timedelta(seconds=interval)
            
            c_val = round(cart_value, 2) if len(cart_items) > 0 else None
            is_post_shipping = e_type in ["shipping_view", "payment_select", "payment_attempt", "payment_failed", "payment_success", "order_completed"]
            s_cost = round(shipping_cost, 2) if (shipping_cost is not None and is_post_shipping) else None
            d_amt = round(discount_amount, 2) if discount_amount > 0 else None
            
            e_dict = {
                "event_id": f"EVT-{event_counter:09d}",
                "session_id": session_id,
                "customer_id": cust_id,
                "event_timestamp": curr_time.isoformat(sep=" "),
                "event_sequence": seq,
                "event_type": e_type,
                "device_type": device_type,
                "customer_type": cust_type,
                "acquisition_channel": acq_channel,
                "product_id": p_id,
                "product_category": p_cat,
                "cart_value": c_val,
                "shipping_cost": s_cost,
                "discount_code": discount_code,
                "discount_amount": d_amt,
                "payment_method": p_method,
                "error_code": err_code,
                "error_message": err_msg,
                "time_since_previous_event": interval
            }
            all_events.append(e_dict)
            seq += 1
            event_counter += 1

        # Event 1: session_start
        add_event("session_start", interval=0)
        
        # -------------------------------------------------------------
        # STAGE 1: Discovery & Browsing
        # -------------------------------------------------------------
        # Browsing depth: Geometric distribution with realistic variation
        num_views = max(1, int(np.random.geometric(p=0.36)))
        # Bouncers exit after 1 view without cart
        will_bounce = (np.random.random() < 0.42)
        
        for v in range(num_views):
            chosen_prod = product_records[np.random.choice(num_prods, p=zipf_probs)]
            add_event("product_view", p_id=chosen_prod["product_id"], p_cat=chosen_prod["category"])
            
            if not will_bounce:
                # Probability of adding to cart after viewing (moderate, ~20-30%)
                p_add = 0.28 if cust_type == "returning" else 0.22
                if np.random.random() < p_add:
                    cart_items.append(chosen_prod)
                    cart_value += chosen_prod["base_price"]
                    add_event("add_to_cart", p_id=chosen_prod["product_id"], p_cat=chosen_prod["category"])
                    
                    # Optional cart view
                    if np.random.random() < 0.65:
                        add_event("cart_view")
                    break # proceed toward checkout evaluation
                    
        # If no item was added, session ends in browsing stage
        if len(cart_items) == 0:
            dropoff_stage = "browsing"
            add_event("session_exit")
            
            # Record session summary
            all_sessions.append({
                "session_id": session_id,
                "customer_id": cust_id,
                "customer_type": cust_type,
                "device_type": device_type,
                "browser": browser,
                "acquisition_channel": acq_channel,
                "session_start_time": session_start_time.isoformat(sep=" "),
                "session_end_time": curr_time.isoformat(sep=" "),
                "session_duration_seconds": int((curr_time - session_start_time).total_seconds()),
                "total_events": seq - 1,
                "reached_cart": False,
                "reached_checkout": False,
                "reached_payment": False,
                "is_purchased": False,
                "final_cart_value": None,
                "dropoff_stage": dropoff_stage
            })
            continue

        # -------------------------------------------------------------
        # STAGE 2: Cart & Checkout Initiation
        # -------------------------------------------------------------
        dropoff_stage = "cart"
        
        # Check if user applies discount promo code
        if np.random.random() < 0.22:
            code_name = np.random.choice(list(DISCOUNT_CODES.keys()), p=[0.4, 0.25, 0.15, 0.12, 0.08])
            code_info = DISCOUNT_CODES[code_name]
            discount_code = code_name
            
            if code_info["valid"]:
                if code_info["amount_type"] == "pct":
                    discount_amount = round(cart_value * code_info["val"], 2)
                elif code_info["amount_type"] == "fixed":
                    discount_amount = min(cart_value, code_info["val"])
                add_event("promo_applied")
            else:
                add_event("promo_applied", err_code="ERR_INVALID_PROMO", err_msg="Promotional discount code is invalid or expired")
                # Friction: invalid promo can trigger slight abandonment
                if np.random.random() < 0.35:
                    add_event("session_exit")
                    all_sessions.append({
                        "session_id": session_id,
                        "customer_id": cust_id,
                        "customer_type": cust_type,
                        "device_type": device_type,
                        "browser": browser,
                        "acquisition_channel": acq_channel,
                        "session_start_time": session_start_time.isoformat(sep=" "),
                        "session_end_time": curr_time.isoformat(sep=" "),
                        "session_duration_seconds": int((curr_time - session_start_time).total_seconds()),
                        "total_events": seq - 1,
                        "reached_cart": True,
                        "reached_checkout": False,
                        "reached_payment": False,
                        "is_purchased": False,
                        "final_cart_value": round(cart_value, 2),
                        "dropoff_stage": dropoff_stage
                    })
                    continue

        # Cart-to-Checkout transition probability (moderate, ~55-70%)
        p_checkout = 0.68 if cust_type == "returning" else 0.58
        if np.random.random() > p_checkout:
            # Abandon at cart
            add_event("session_exit")
            all_sessions.append({
                "session_id": session_id,
                "customer_id": cust_id,
                "customer_type": cust_type,
                "device_type": device_type,
                "browser": browser,
                "acquisition_channel": acq_channel,
                "session_start_time": session_start_time.isoformat(sep=" "),
                "session_end_time": curr_time.isoformat(sep=" "),
                "session_duration_seconds": int((curr_time - session_start_time).total_seconds()),
                "total_events": seq - 1,
                "reached_cart": True,
                "reached_checkout": False,
                "reached_payment": False,
                "is_purchased": False,
                "final_cart_value": round(cart_value, 2),
                "dropoff_stage": dropoff_stage
            })
            continue

        # Proceed to Checkout
        add_event("checkout_start")
        
        # Backtracking chance from checkout start back to cart
        if np.random.random() < 0.04:
            add_event("cart_view")
            add_event("checkout_start")

        # -------------------------------------------------------------
        # STAGE 3: Address Entry & Fulfillment
        # -------------------------------------------------------------
        dropoff_stage = "address"
        add_event("address_entry")
        
        # Address progression probability: slight mobile input friction (~75% vs ~84% desktop)
        p_address_pass = 0.77 if device_type == "mobile" else 0.85
        if cust_type == "returning":
            p_address_pass += 0.05 # returning users have saved address
            
        if np.random.random() > p_address_pass:
            # Abandon at address entry
            add_event("session_exit")
            all_sessions.append({
                "session_id": session_id,
                "customer_id": cust_id,
                "customer_type": cust_type,
                "device_type": device_type,
                "browser": browser,
                "acquisition_channel": acq_channel,
                "session_start_time": session_start_time.isoformat(sep=" "),
                "session_end_time": curr_time.isoformat(sep=" "),
                "session_duration_seconds": int((curr_time - session_start_time).total_seconds()),
                "total_events": seq - 1,
                "reached_cart": True,
                "reached_checkout": True,
                "reached_payment": False,
                "is_purchased": False,
                "final_cart_value": round(cart_value, 2),
                "dropoff_stage": dropoff_stage
            })
            continue

        # -------------------------------------------------------------
        # STAGE 4: Shipping Selection & Cost Calculation
        # -------------------------------------------------------------
        dropoff_stage = "shipping"
        
        # Compute shipping fee based on max weight tier and cart value
        weight_tiers = [item["shipping_weight_tier"] for item in cart_items]
        highest_weight = "oversized" if "oversized" in weight_tiers else ("heavy" if "heavy" in weight_tiers else ("medium" if "medium" in weight_tiers else "light"))
        base_ship = SHIPPING_BASE_RATES[highest_weight]
        
        if cart_value >= FREE_SHIPPING_THRESHOLD or discount_code == "FREESHIP":
            shipping_cost = 0.0
        else:
            shipping_cost = base_ship
            
        add_event("shipping_view")
        
        # Shipping fee ratio friction: shipping_cost / cart_value
        ship_ratio = shipping_cost / max(cart_value, 1.0)
        
        # Probabilistic drop-off sensitive to shipping ratio
        # Base shipping pass rate is ~88%, decaying moderately with high shipping ratio
        p_ship_pass = max(0.45, 0.90 - (ship_ratio * 0.75))
        if shipping_cost == 0.0:
            p_ship_pass = 0.94
            
        if np.random.random() > p_ship_pass:
            # Backtrack check: user may backtrack to add items for free shipping
            if cart_value < FREE_SHIPPING_THRESHOLD and np.random.random() < 0.15:
                add_event("cart_view")
                chosen_extra = product_records[np.random.choice(num_prods, p=zipf_probs)]
                cart_items.append(chosen_extra)
                cart_value += chosen_extra["base_price"]
                add_event("add_to_cart", p_id=chosen_extra["product_id"], p_cat=chosen_extra["category"])
                add_event("checkout_start")
                add_event("address_entry")
                if cart_value >= FREE_SHIPPING_THRESHOLD:
                    shipping_cost = 0.0
                add_event("shipping_view")
            else:
                # Abandon at shipping
                add_event("session_exit")
                all_sessions.append({
                    "session_id": session_id,
                    "customer_id": cust_id,
                    "customer_type": cust_type,
                    "device_type": device_type,
                    "browser": browser,
                    "acquisition_channel": acq_channel,
                    "session_start_time": session_start_time.isoformat(sep=" "),
                    "session_end_time": curr_time.isoformat(sep=" "),
                    "session_duration_seconds": int((curr_time - session_start_time).total_seconds()),
                    "total_events": seq - 1,
                    "reached_cart": True,
                    "reached_checkout": True,
                    "reached_payment": False,
                    "is_purchased": False,
                    "final_cart_value": round(cart_value, 2),
                    "dropoff_stage": dropoff_stage
                })
                continue

        # -------------------------------------------------------------
        # STAGE 5: Payment Method Selection & Execution
        # -------------------------------------------------------------
        dropoff_stage = "payment"
        
        # Payment Method Choice
        if cust.get("default_payment_preference") and np.random.random() < 0.70:
            active_payment_method = cust["default_payment_preference"]
        else:
            # High cart value (> $200) slightly favors BNPL / Credit Card
            if cart_value > 200.0:
                p_methods = [0.45, 0.18, 0.10, 0.22, 0.05]
            else:
                p_methods = PAYMENT_METHOD_PROBS
            active_payment_method = np.random.choice(PAYMENT_METHODS, p=p_methods)
            
        add_event("payment_select", p_method=active_payment_method)
        
        # Pre-attempt drop-off (hesitation/review) ~6%
        if np.random.random() < 0.06:
            add_event("session_exit")
            all_sessions.append({
                "session_id": session_id,
                "customer_id": cust_id,
                "customer_type": cust_type,
                "device_type": device_type,
                "browser": browser,
                "acquisition_channel": acq_channel,
                "session_start_time": session_start_time.isoformat(sep=" "),
                "session_end_time": curr_time.isoformat(sep=" "),
                "session_duration_seconds": int((curr_time - session_start_time).total_seconds()),
                "total_events": seq - 1,
                "reached_cart": True,
                "reached_checkout": True,
                "reached_payment": False,
                "is_purchased": False,
                "final_cart_value": round(cart_value, 2),
                "dropoff_stage": dropoff_stage
            })
            continue

        # Payment Execution & Retry Simulation (up to 3 attempts)
        payment_resolved = False
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts and not payment_resolved:
            attempts += 1
            add_event("payment_attempt", p_method=active_payment_method)
            
            # Baseline failure rates by instrument:
            # Credit Card ~6.5%, Debit ~8.5%, NetBanking ~10%, Wallet ~3.5%, BNPL ~5.5%
            fail_rates = {
                "credit_card": 0.065,
                "debit_card": 0.085,
                "net_banking": 0.105,
                "digital_wallet": 0.035,
                "bnpl": 0.055
            }
            base_fail = fail_rates.get(active_payment_method, 0.07)
            # High cart value (> $300) slightly increases card limit declines
            if cart_value > 300.0 and active_payment_method in ["credit_card", "debit_card"]:
                base_fail += 0.035
                
            is_failed = (np.random.random() < base_fail)
            
            if not is_failed:
                # Payment Succeeded!
                add_event("payment_success", p_method=active_payment_method)
                add_event("order_completed", p_method=active_payment_method)
                add_event("session_exit")
                dropoff_stage = "converted"
                is_purchased = True
                payment_resolved = True
            else:
                # Payment Failed
                err_code, err_msg = PAYMENT_ERRORS[np.random.choice(len(PAYMENT_ERRORS))]
                add_event("payment_failed", p_method=active_payment_method, err_code=err_code, err_msg=err_msg)
                
                # Customer Reaction Post-Failure:
                # 45% abandon, 35% retry same method, 20% switch method
                reaction = np.random.choice(["abandon", "retry_same", "switch_method"], p=[0.46, 0.34, 0.20])
                
                if reaction == "abandon" or attempts >= max_attempts:
                    add_event("session_exit")
                    payment_resolved = True # end loop
                elif reaction == "retry_same":
                    # User attempts another payment with the same method
                    pass # loop continues to next attempt
                elif reaction == "switch_method":
                    # User selects alternative method
                    other_methods = [m for m in PAYMENT_METHODS if m != active_payment_method]
                    active_payment_method = np.random.choice(other_methods)
                    add_event("payment_select", p_method=active_payment_method)

        # Record finalized session
        all_sessions.append({
            "session_id": session_id,
            "customer_id": cust_id,
            "customer_type": cust_type,
            "device_type": device_type,
            "browser": browser,
            "acquisition_channel": acq_channel,
            "session_start_time": session_start_time.isoformat(sep=" "),
            "session_end_time": curr_time.isoformat(sep=" "),
            "session_duration_seconds": int((curr_time - session_start_time).total_seconds()),
            "total_events": seq - 1,
            "reached_cart": True,
            "reached_checkout": True,
            "reached_payment": True,
            "is_purchased": is_purchased,
            "final_cart_value": round(cart_value, 2),
            "dropoff_stage": dropoff_stage
        })

    df_events = pd.DataFrame(all_events)
    df_sessions = pd.DataFrame(all_sessions)
    return df_sessions, df_events

# ----------------------------------------------------------------------
# 4. Master Orchestration & Persistence
# ----------------------------------------------------------------------
def main():
    print("================================================================")
    print("  ShopSphere Synthetic Data Generation Pipeline (Phase 2)")
    print(f"  Fixed Master Seed: {MASTER_SEED}")
    print("================================================================")
    
    # 1. Products
    print("[1/4] Generating product catalog...")
    df_products = generate_products(total_products=180)
    
    # 2. Customers
    print("[2/4] Generating customer population...")
    df_customers = generate_customers(num_customers=50000)
    
    # 3. Sessions & Events Clickstream
    print("[3/4] Generating 120,000 sessions and clickstream event sequences...")
    df_sessions, df_events = simulate_event_stream(
        num_sessions=120000,
        df_customers=df_customers,
        df_products=df_products
    )
    
    # 4. Save Raw Datasets (CSV)
    print("[4/4] Writing raw CSV datasets to data/raw/ ...")
    raw_cust_path = os.path.join(RAW_DATA_DIR, "customers.csv")
    raw_prod_path = os.path.join(RAW_DATA_DIR, "products.csv")
    raw_sess_path = os.path.join(RAW_DATA_DIR, "sessions.csv")
    raw_evt_path = os.path.join(RAW_DATA_DIR, "events.csv")
    
    df_customers.to_csv(raw_cust_path, index=False)
    df_products.to_csv(raw_prod_path, index=False)
    df_sessions.to_csv(raw_sess_path, index=False)
    df_events.to_csv(raw_evt_path, index=False)
    print(f"      -> Saved: {raw_cust_path} ({len(df_customers):,} rows)")
    print(f"      -> Saved: {raw_prod_path} ({len(df_products):,} rows)")
    print(f"      -> Saved: {raw_sess_path} ({len(df_sessions):,} rows)")
    print(f"      -> Saved: {raw_evt_path} ({len(df_events):,} rows)")
    
    # 5. Save Processed Datasets (Parquet & CSV)
    print("      Writing analysis-ready Parquet datasets to data/processed/ ...")
    proc_cust_path = os.path.join(PROCESSED_DATA_DIR, "customers.parquet")
    proc_prod_path = os.path.join(PROCESSED_DATA_DIR, "products.parquet")
    proc_sess_path = os.path.join(PROCESSED_DATA_DIR, "sessions.parquet")
    proc_evt_path = os.path.join(PROCESSED_DATA_DIR, "events.parquet")
    
    df_customers.to_parquet(proc_cust_path, index=False, engine="pyarrow")
    df_products.to_parquet(proc_prod_path, index=False, engine="pyarrow")
    df_sessions.to_parquet(proc_sess_path, index=False, engine="pyarrow")
    df_events.to_parquet(proc_evt_path, index=False, engine="pyarrow")
    print(f"      -> Saved: {proc_cust_path}")
    print(f"      -> Saved: {proc_prod_path}")
    print(f"      -> Saved: {proc_sess_path}")
    print(f"      -> Saved: {proc_evt_path}")
    
    print("\n[OK] Synthetic data generation complete with 100% reproducibility.")

if __name__ == "__main__":
    main()
