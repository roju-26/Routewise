import pandas as pd


# ============================================================
# 1. LOAD ORDERS
# ============================================================

orders = pd.read_csv("data/orders.csv")


# ============================================================
# 2. CALCULATE TIME WINDOW
# ============================================================

orders["time_window_minutes"] = (
    orders["due_time"] - orders["ready_time"]
)


# ============================================================
# 3. ESTIMATE TRAVEL TIME
# ============================================================

orders["distance_from_depot"] = (
    (orders["x"] ** 2 + orders["y"] ** 2) ** 0.5
)

orders["estimated_travel_time_min"] = (
    orders["distance_from_depot"] * 2
)


# ============================================================
# 4. TRAVEL-TIME PRESSURE
# ============================================================

orders["travel_time_ratio"] = (
    orders["estimated_travel_time_min"]
    / orders["time_window_minutes"]
)


# ============================================================
# 5. RISK CALCULATION
# ============================================================

orders["travel_risk"] = (
    orders["travel_time_ratio"] * 100
).clip(0, 100)

orders["historical_risk"] = (
    orders["historical_late_rate"] * 100
)

orders["time_window_risk"] = (
    (360 - orders["time_window_minutes"]) / 360
) * 100

orders["time_window_risk"] = (
    orders["time_window_risk"].clip(0, 100)
)


orders["risk_score"] = (
    0.40 * orders["travel_risk"]
    + 0.40 * orders["historical_risk"]
    + 0.20 * orders["time_window_risk"]
).round(2)


# ============================================================
# 6. RISK LEVEL
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
# 7. CRITICAL DELIVERY
# ============================================================

orders["critical"] = (
    (orders["priority"] == "High")
    |
    (orders["time_window_minutes"] <= 60)
    |
    (orders["travel_time_ratio"] >= 0.8)
)


# ============================================================
# 8. CRITICAL REASONS
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
# 9. RECOMMENDATION
# ============================================================

def get_recommendation(row):

    if row["risk_level"] == "High" and row["critical"]:
        return "Immediate attention"

    elif row["risk_level"] == "High":
        return "Monitor closely"

    elif row["risk_level"] == "Medium" and row["critical"]:
        return "Prioritize delivery"

    elif row["risk_level"] == "Medium":
        return "Monitor"

    elif row["risk_level"] == "Low" and row["critical"]:
        return "Prioritize due to critical condition"

    else:
        return "Normal delivery"


orders["recommendation"] = (
    orders.apply(get_recommendation, axis=1)
)


# ============================================================
# 10. EVIDENCE / REASON
# ============================================================

def get_evidence(row):

    evidence = []

    if row["risk_level"] == "High":
        evidence.append(
            f"High risk score ({row['risk_score']})"
        )

    elif row["risk_level"] == "Medium":
        evidence.append(
            f"Medium risk score ({row['risk_score']})"
        )

    if row["historical_late_rate"] >= 0.30:
        evidence.append(
            f"Historical late rate {row['historical_late_rate'] * 100:.0f}%"
        )

    if row["time_window_minutes"] <= 60:
        evidence.append(
            "Tight delivery window"
        )

    if row["travel_time_ratio"] >= 0.8:
        evidence.append(
            "High travel-time pressure"
        )

    if row["priority"] == "High":
        evidence.append(
            "High priority order"
        )

    if not evidence:
        evidence.append(
            "No major risk indicators"
        )

    return "; ".join(evidence)


orders["evidence"] = (
    orders.apply(get_evidence, axis=1)
)


# ============================================================
# 11. DISPLAY RESULTS
# ============================================================

print("\nEvidence-Based Recommendations:")

print(
    orders[
        [
            "order_id",
            "risk_level",
            "risk_score",
            "priority",
            "critical",
            "recommendation",
            "evidence"
        ]
    ].to_string(index=False)
)


# ============================================================
# 12. RECOMMENDATION SUMMARY
# ============================================================

print("\nRecommendation Summary:")

print(
    orders["recommendation"].value_counts()
)