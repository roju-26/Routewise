import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

orders = pd.read_csv("data/orders.csv")
vehicles = pd.read_csv("data/vehicles.csv")


# ============================================================
# 2. VEHICLE CAPACITY CHECK
# ============================================================

max_vehicle_capacity = vehicles["capacity"].max()

orders["capacity_exception"] = (
    orders["weight"] > max_vehicle_capacity
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


orders["time_window_exception"] = (
    orders["estimated_travel_time_min"]
    > orders["time_window_minutes"]
)


# ============================================================
# 5. COMBINE EXCEPTIONS
# ============================================================

orders["exception"] = (
    orders["capacity_exception"]
    |
    orders["time_window_exception"]
)


# ============================================================
# 6. GENERATE EXCEPTION REASONS
# ============================================================

def get_exception_reason(row):

    reasons = []

    if row["capacity_exception"]:
        reasons.append(
            f"Order weight ({row['weight']}) exceeds maximum vehicle capacity ({max_vehicle_capacity})"
        )

    if row["time_window_exception"]:
        reasons.append(
            f"Estimated travel time ({row['estimated_travel_time_min']:.1f} min) exceeds delivery window ({row['time_window_minutes']} min)"
        )

    return "; ".join(reasons)


orders["exception_reason"] = (
    orders.apply(get_exception_reason, axis=1)
)


# ============================================================
# 7. DISPLAY EXCEPTIONS
# ============================================================

exception_orders = orders[
    orders["exception"]
]


print("\nException Analysis:")

if len(exception_orders) == 0:

    print("No exceptions detected.")

else:

    print(
        exception_orders[
            [
                "order_id",
                "weight",
                "time_window_minutes",
                "estimated_travel_time_min",
                "exception_reason"
            ]
        ].to_string(index=False)
    )


# ============================================================
# 8. SUMMARY
# ============================================================

print("\nException Summary:")

print(
    "Total orders:",
    len(orders)
)

print(
    "Orders with exceptions:",
    len(exception_orders)
)

print(
    "Orders without exceptions:",
    len(orders) - len(exception_orders)
)
# ============================================================
# RETURN EXCEPTION DATA FOR OTHER MODULES
# ============================================================

def get_exception_data():
    return orders[
        [
            "order_id",
            "weight",
            "time_window_minutes",
            "estimated_travel_time_min",
            "capacity_exception",
            "time_window_exception",
            "exception",
            "exception_reason"
        ]
    ].copy()