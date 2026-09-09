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

print("\nDelivery Time Window:")
print(
    orders[
        [
            "order_id",
            "ready_time",
            "due_time",
            "time_window_minutes"
        ]
    ].head(10)
)


# ============================================================
# 3. ESTIMATE TRAVEL TIME
# ============================================================

# Depot is at (0, 0)
orders["distance_from_depot"] = (
    (orders["x"] ** 2 + orders["y"] ** 2) ** 0.5
)

# Same travel-time assumption used by the optimizer
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

print("\nTravel Time Analysis:")
print(
    orders[
        [
            "order_id",
            "time_window_minutes",
            "estimated_travel_time_min",
            "travel_time_ratio"
        ]
    ].head(10)
)


# ============================================================
# 5. HISTORICAL LATE RATE
# ============================================================



orders["historical_late_rate_percent"] = (
    orders["historical_late_rate"] * 100
)

print("\nHistorical Late Rate:")
print(
    orders[
        [
            "order_id",
            "historical_late_rate",
            "historical_late_rate_percent"
        ]
    ].head(10)
)


# ============================================================
# 6. TRAVEL RISK
# ============================================================

orders["travel_risk"] = (
    orders["travel_time_ratio"] * 100
)

orders["travel_risk"] = (
    orders["travel_risk"].clip(0, 100)
)


# ============================================================
# 7. HISTORICAL RISK
# ============================================================

orders["historical_risk"] = (
    orders["historical_late_rate"] * 100
)

# 8. TIME WINDOW RISK

# Smaller delivery windows mean higher risk.
orders["time_window_risk"] = (
    (360 - orders["time_window_minutes"]) / 360
) * 100

orders["time_window_risk"] = (
    orders["time_window_risk"].clip(0, 100)
)


# ============================================================
# 9. FINAL RISK SCORE
# ============================================================

orders["risk_score"] = (
    0.40 * orders["travel_risk"]
    + 0.40 * orders["historical_risk"]
    + 0.20 * orders["time_window_risk"]
)

orders["risk_score"] = (
    orders["risk_score"].round(2)
)


# ============================================================
# 10. CLASSIFY RISK
# ============================================================

def classify_risk(score):

    if score < 20:
        return "Low"

    elif score < 30:
        return "Medium"

    else:
        return "High"


orders["risk_level"] = (
    orders["risk_score"].apply(classify_risk)
)


# ============================================================
# 11. DISPLAY RISK RESULTS
# ============================================================

print("\nRisk Prediction:")

print(
    orders[
        [
            "order_id",
            "travel_risk",
            "historical_risk",
            "time_window_risk",
            "risk_score",
            "risk_level"
        ]
    ].head(10)
)


# ============================================================
# 12. RISK LEVEL SUMMARY
# ============================================================

print("\nRisk Level Summary:")

print(
    orders["risk_level"].value_counts()
)


# ============================================================
# 13. RISK SCORE DISTRIBUTION
# ============================================================

print("\nRisk Score Distribution:")

print(
    orders["risk_score"].describe()
)
# ============================================================
# RETURN DATA FOR OTHER MODULES
# ============================================================

def get_risk_data():
    return orders[
        [
            "order_id",
            "risk_score",
            "risk_level",
            "historical_late_rate",
            "travel_time_ratio",
            "time_window_minutes"
        ]
    ].copy()