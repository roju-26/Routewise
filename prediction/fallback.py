import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

orders = pd.read_csv("data/orders.csv")
vehicles = pd.read_csv("data/vehicles.csv")


# ============================================================
# 2. VEHICLE CAPACITY CHECK
# ============================================================

max_capacity = vehicles["capacity"].max()

orders["capacity_issue"] = (
    orders["weight"] > max_capacity
)


# ============================================================
# 3. TIME WINDOW CHECK
# ============================================================

orders["time_window_minutes"] = (
    orders["due_time"] - orders["ready_time"]
)


# ============================================================
# 4. ESTIMATE TRAVEL TIME
# ============================================================

orders["distance_from_depot"] = (
    (orders["x"] ** 2 + orders["y"] ** 2) ** 0.5
)

orders["estimated_travel_time_min"] = (
    orders["distance_from_depot"] * 2
)


orders["time_window_issue"] = (
    orders["estimated_travel_time_min"]
    > orders["time_window_minutes"]
)


# ============================================================
# 5. FALLBACK DECISION
# ============================================================

def get_fallback(row):

    # Case 1: Vehicle capacity problem
    if row["capacity_issue"]:

        return "Use larger vehicle or split delivery"

    # Case 2: Time-window problem
    elif row["time_window_issue"]:

        return "Prioritize order or use nearest available vehicle"

    # Case 3: No exception
    else:

        return "No fallback required"


orders["fallback_action"] = (
    orders.apply(get_fallback, axis=1)
)


# ============================================================
# 6. FALLBACK REASON
# ============================================================

def get_fallback_reason(row):

    reasons = []

    if row["capacity_issue"]:

        reasons.append(
            f"Weight {row['weight']} exceeds maximum capacity {max_capacity}"
        )

    if row["time_window_issue"]:

        reasons.append(
            f"Travel time {row['estimated_travel_time_min']:.1f} min exceeds available window {row['time_window_minutes']} min"
        )

    if not reasons:

        reasons.append(
            "No direct capacity or time-window violation"
        )

    return "; ".join(reasons)


orders["fallback_reason"] = (
    orders.apply(get_fallback_reason, axis=1)
)


# ============================================================
# 7. DISPLAY FALLBACK INFORMATION
# ============================================================

print("\nFallback Handling:")

print(
    orders[
        orders["capacity_issue"] |
        orders["time_window_issue"]
    ][
        [
            "order_id",
            "weight",
            "time_window_minutes",
            "estimated_travel_time_min",
            "fallback_action",
            "fallback_reason"
        ]
    ].to_string(index=False)
)

# ============================================================
# 8. SUMMARY
# ============================================================

print("\nFallback Summary:")

print(
    "Total orders:",
    len(orders)
)

print(
    "Orders requiring fallback:",
    (
        orders["capacity_issue"]
        |
        orders["time_window_issue"]
    ).sum()
)
# ============================================================
# RETURN FALLBACK DATA FOR OTHER MODULES
# ============================================================

def get_fallback_data():
    return orders[
        [
            "order_id",
            "capacity_issue",
            "time_window_issue",
            "fallback_action",
            "fallback_reason"
        ]
    ].copy()