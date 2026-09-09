import pandas as pd

# ============================================================
# 1. LOAD ORDERS
# ============================================================

orders = pd.read_csv("data/orders.csv")


# ============================================================
# 2. CALCULATE DELIVERY TIME WINDOW
# ============================================================

orders["time_window_minutes"] = (
    orders["due_time"] - orders["ready_time"]
)


# ============================================================
# 3. ESTIMATE TRAVEL TIME
# ============================================================

# Depot is at (0, 0)

orders["distance_from_depot"] = (
    (orders["x"] ** 2 + orders["y"] ** 2) ** 0.5
)

# Same assumption used by optimizer

orders["estimated_travel_time_min"] = (
    orders["distance_from_depot"] * 2
)


# ============================================================
# 4. CALCULATE TRAVEL-TIME PRESSURE
# ============================================================

orders["travel_time_ratio"] = (
    orders["estimated_travel_time_min"]
    / orders["time_window_minutes"]
)


# ============================================================
# 5. IDENTIFY CRITICAL ORDERS
# ============================================================

orders["critical"] = (
    (orders["priority"] == "High")
    |
    (orders["time_window_minutes"] <= 60)
    |
    (orders["travel_time_ratio"] >= 0.8)
)


# ============================================================
# 6. GENERATE CRITICAL REASONS
# ============================================================

def get_critical_reasons(row):

    reasons = []

    if row["priority"] == "High":
        reasons.append("High priority")

    if row["time_window_minutes"] <= 60:
        reasons.append("Tight time window")

    if row["travel_time_ratio"] >= 0.8:
        reasons.append("High travel-time pressure")

    return ", ".join(reasons)


orders["critical_reason"] = (
    orders.apply(get_critical_reasons, axis=1)
)


# ============================================================
# 7. GET CRITICAL ORDERS
# ============================================================

critical_orders = orders[
    orders["critical"]
]


# ============================================================
# 8. DISPLAY RESULTS
# ============================================================

print("\nCritical Delivery Analysis:")

print(
    critical_orders[
        [
            "order_id",
            "priority",
            "time_window_minutes",
            "travel_time_ratio",
            "critical_reason"
        ]
    ].to_string(index=False)
)



# 9. SUMMARY

print("\nCritical Delivery Summary:")

print(
    "Total orders:",
    len(orders)
)

print(
    "Critical orders:",
    len(critical_orders)
)

print(
    "Non-critical orders:",
    len(orders) - len(critical_orders)
)
# ============================================================
# RETURN CRITICAL DELIVERY DATA FOR OTHER MODULES
# ============================================================

def get_critical_data():
    return orders[
        [
            "order_id",
            "priority",
            "time_window_minutes",
            "travel_time_ratio",
            "critical",
            "critical_reason"
        ]
    ].copy()