# ShopSphere Data Dictionary

This document provides a comprehensive data dictionary for all tables and attributes in the ShopSphere analytics data model, detailing data types, allowable ranges, nullability constraints, derivation rules, and business definitions.

---

## Table of Contents
1. [`customers` Table](#1-customers-table)
2. [`products` Table](#2-products-table)
3. [`sessions` Table](#3-sessions-table)
4. [`events` Table](#4-events-table)

---

## 1. `customers` Table
- **Purpose:** Customer dimension entity capturing customer maturity, account status, historical transaction frequency, and saved checkout preferences.
- **Grain:** 1 record per unique customer.
- **Primary Key:** `customer_id`

| Field Name | Data Type | Nullable | Derived? | Allowed Values / Format | Business Meaning & Usage |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `customer_id` | VARCHAR(64) | No | No | `CUST-000001` ... `CUST-999999` | Unique persistent identifier assigned to each customer profile. |
| `customer_type` | VARCHAR(20) | No | No | `new`, `returning` | Customer classification based on historical interaction with ShopSphere. |
| `account_created_at` | TIMESTAMP | Yes | No | ISO 8601 string (`YYYY-MM-DD HH:MM:SS`) | Timestamp when customer registered their profile. NULL for guest visitors. |
| `lifetime_orders` | INTEGER | No | No | $\ge 0$ (Integer) | Count of successful orders placed by this customer prior to current session. |
| `default_payment_preference` | VARCHAR(30) | Yes | No | `credit_card`, `digital_wallet`, `debit_card`, `bnpl`, `net_banking` | Saved payment instrument on customer profile. NULL if unassigned. |

---

## 2. `products` Table
- **Purpose:** Product catalog dimension detailing SKU identifiers, categories, retail base prices, and logistics weight tiers.
- **Grain:** 1 record per SKU.
- **Primary Key:** `product_id`

| Field Name | Data Type | Nullable | Derived? | Allowed Values / Format | Business Meaning & Usage |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `product_id` | VARCHAR(64) | No | No | `PROD-0001` ... `PROD-9999` | Unique SKU identifier. |
| `product_name` | VARCHAR(150) | No | No | Text string | Official merchant catalog title. |
| `category` | VARCHAR(50) | No | No | `Electronics`, `Fashion & Apparel`, `Home & Kitchen`, `Beauty & Personal Care`, `Sports & Fitness`, `Books & Stationery` | High-level product category classification. |
| `base_price` | DECIMAL(10,2) | No | No | $8.00 – $650.00 | Standard listing price in USD. |
| `shipping_weight_tier` | VARCHAR(20) | No | No | `light`, `medium`, `heavy`, `oversized` | Logistics classification determining base fulfillment surcharge. |

---

## 3. `sessions` Table
- **Purpose:** Aggregated session fact table capturing session-level acquisition attributes, device context, progression flags, duration, and conversion outcomes.
- **Grain:** 1 record per unique customer browsing session.
- **Primary Key:** `session_id`
- **Foreign Key:** `customer_id` → `customers.customer_id`

| Field Name | Data Type | Nullable | Derived? | Allowed Values / Format | Business Meaning & Usage |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `session_id` | VARCHAR(64) | No | No | `SESS-0000001` ... | Unique session identifier. |
| `customer_id` | VARCHAR(64) | No | No | `CUST-XXXXXX` | Reference to customer initiating the session. |
| `customer_type` | VARCHAR(20) | No | Yes | `new`, `returning` | Customer classification at time of session. |
| `device_type` | VARCHAR(20) | No | No | `mobile`, `desktop`, `tablet` | Device hardware category. |
| `browser` | VARCHAR(30) | Yes | No | `Chrome`, `Safari`, `Edge`, `Firefox`, `Chrome Mobile`, `Safari Mobile`, `Samsung Internet` | Browser application used. |
| `acquisition_channel` | VARCHAR(30) | No | No | `organic_search`, `paid_search`, `paid_social`, `direct`, `email_crm`, `affiliate` | Last-touch inbound traffic channel. |
| `session_start_time` | TIMESTAMP | No | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp of first event in session. |
| `session_end_time` | TIMESTAMP | No | Yes | `YYYY-MM-DD HH:MM:SS` | Timestamp of final event in session. |
| `session_duration_seconds` | INTEGER | No | Yes | $\ge 0$ | Total session duration in seconds (`session_end_time - session_start_time`). |
| `total_events` | INTEGER | No | Yes | $\ge 1$ | Total count of clickstream events in session. |
| `reached_cart` | BOOLEAN | No | Yes | `TRUE`, `FALSE` | Flag indicating whether $\ge 1$ `add_to_cart` occurred. |
| `reached_checkout` | BOOLEAN | No | Yes | `TRUE`, `FALSE` | Flag indicating whether `checkout_start` occurred. |
| `reached_payment` | BOOLEAN | No | Yes | `TRUE`, `FALSE` | Flag indicating whether `payment_attempt` occurred. |
| `is_purchased` | BOOLEAN | No | Yes | `TRUE`, `FALSE` | Flag indicating whether `order_completed` was achieved. |
| `final_cart_value` | DECIMAL(10,2) | Yes | Yes | $\ge 0.00$ or `NULL` | Final merchandise total in cart at session close or order completion. |
| `dropoff_stage` | VARCHAR(30) | No | Yes | `browsing`, `cart`, `address`, `shipping`, `payment`, `converted` | Stage at which user terminated their journey. |

---

## 4. `events` Table
- **Purpose:** Fine-grained behavioral clickstream fact table tracking every discrete action, micro-step, payment attempt, error state, and dwell duration.
- **Grain:** 1 record per user action/event.
- **Primary Key:** `event_id`
- **Foreign Keys:** `session_id` → `sessions.session_id`, `customer_id` → `customers.customer_id`, `product_id` → `products.product_id`

| Field Name | Data Type | Nullable | Derived? | Allowed Values / Format | Business Meaning & Usage |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `event_id` | VARCHAR(64) | No | No | `EVT-000000001` ... | Unique clickstream event record ID. |
| `session_id` | VARCHAR(64) | No | No | `SESS-XXXXXXX` | Parent session reference. |
| `customer_id` | VARCHAR(64) | No | No | `CUST-XXXXXX` | Reference to customer. |
| `event_timestamp` | TIMESTAMP | No | No | `YYYY-MM-DD HH:MM:SS` | Exact wall-clock timestamp of event occurrence. |
| `event_sequence` | INTEGER | No | No | $1, 2, 3, \dots N$ | 1-indexed sequential event ordering within the session. |
| `event_type` | VARCHAR(50) | No | No | `session_start`, `product_view`, `add_to_cart`, `cart_view`, `promo_applied`, `checkout_start`, `address_entry`, `shipping_view`, `payment_select`, `payment_attempt`, `payment_failed`, `payment_success`, `order_completed`, `session_exit` | Name of user action / funnel stage milestone. |
| `device_type` | VARCHAR(20) | No | No | `mobile`, `desktop`, `tablet` | Denormalized device identifier for fast event filtering. |
| `customer_type` | VARCHAR(20) | No | No | `new`, `returning` | Denormalized customer type identifier. |
| `acquisition_channel` | VARCHAR(30) | No | No | `organic_search`, `paid_search`, `paid_social`, `direct`, `email_crm`, `affiliate` | Denormalized traffic acquisition channel. |
| `product_id` | VARCHAR(64) | Yes | No | `PROD-XXXX` or `NULL` | Product SKU referenced in browsing/cart events; NULL in pure checkout steps. |
| `product_category` | VARCHAR(50) | Yes | No | Category string or `NULL` | Category of product viewed/added. |
| `cart_value` | DECIMAL(10,2) | Yes | Yes | $\ge 0.00$ or `NULL` | Cumulative active merchandise cart value at time of event. |
| `shipping_cost` | DECIMAL(10,2) | Yes | Yes | $\ge 0.00$ or `NULL` | Calculated shipping fee. NULL prior to `shipping_view`; $0.00 for free shipping. |
| `discount_code` | VARCHAR(30) | Yes | No | `WELCOME10`, `SPHERE20`, `FREESHIP`, `EXPIRED50`, `DEAL100`, or `NULL` | Promo code submitted by user. |
| `discount_amount` | DECIMAL(10,2) | Yes | Yes | $\ge 0.00$ or `NULL` | Applied discount amount in USD. |
| `payment_method` | VARCHAR(30) | Yes | No | `credit_card`, `digital_wallet`, `debit_card`, `bnpl`, `net_banking`, or `NULL` | Selected payment instrument. |
| `error_code` | VARCHAR(50) | Yes | No | `ERR_INSUFFICIENT_FUNDS`, `ERR_GATEWAY_TIMEOUT`, `ERR_3DS_AUTH_FAILED`, `ERR_CARD_EXPIRED`, `ERR_BANK_DECLINE`, `ERR_INVALID_PROMO`, or `NULL` | Machine error code for failed interactions. |
| `error_message` | VARCHAR(255) | Yes | No | Text string or `NULL` | Human-readable explanation of error. |
| `time_since_previous_event` | INTEGER | No | Yes | $\ge 0$ (Seconds) | Elapsed duration in seconds since immediately preceding event ($0$ for `event_sequence = 1`). |
