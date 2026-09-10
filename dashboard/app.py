import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
import os

# Add Routewise project folder to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from prediction.risk import get_risk_data
from prediction.critical import get_critical_data
from prediction.exceptions import get_exception_data
from prediction.fallback import get_fallback_data
from optimization.optimizer import get_optimization_results

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="RouteWise",
    page_icon="🚚",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .rw-header {
        background: linear-gradient(135deg, #111827, #1f2937);
        color: white;
        padding: 26px 28px;
        border-radius: 18px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    .rw-title {
        font-size: 38px;
        font-weight: 800;
        margin: 0;
    }

    .rw-subtitle {
        font-size: 17px;
        color: #d1d5db;
        margin-top: 6px;
    }

    .status-badge {
        display: inline-block;
        margin-top: 12px;
        padding: 6px 12px;
        border-radius: 999px;
        background: #dcfce7;
        color: #166534;
        font-size: 13px;
        font-weight: 700;
    }

    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        min-height: 125px;
    }

    .kpi-label {
        font-size: 13px;
        color: #374151;
        margin-top: 5px;
        font-weight: 700;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        color: #111827;
    }

    .panel {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }

    .panel-title {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 12px;
        color: #0f172a;
        background: #eaf2ff;
        padding: 12px 16px;
        border-radius: 10px;
    }

    .vehicle-card {
        padding: 13px 14px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
        background: #f9fafb;
    }

    .vehicle-name {
        font-size: 15px;
        font-weight: 700;
    }

    .vehicle-details {
        font-size: 13px;
        color: #6b7280;
        margin-top: 3px;
    }

    .risk-high {
        background: #fee2e2;
        color: #991b1b;
        padding: 5px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
    }

    .risk-medium {
        background: #fef3c7;
        color: #92400e;
        padding: 5px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
    }

    .risk-low {
        background: #dcfce7;
        color: #166534;
        padding: 5px 10px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
    }

    .small-note {
        color: #6b7280;
        font-size: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# REAL ROUTEWISE DATA
# ============================================================

orders_df = pd.read_csv("data/orders.csv")
vehicles_df = pd.read_csv("data/vehicles.csv")

risk_df = get_risk_data()
critical_df = get_critical_data()
exception_df = get_exception_data()
fallback_df = get_fallback_data()

optimization_results = get_optimization_results()

optimized_distance = optimization_results["total_distance"]
total_deliveries = optimization_results["total_deliveries"]
total_on_time = optimization_results["on_time"]
total_late = optimization_results["late"]
route_results = optimization_results["routes"]


total_orders = len(orders_df)
total_vehicles = len(vehicles_df)

high_risk_deliveries = (
    risk_df["risk_level"] == "High"
).sum()

# Temporary baseline for optimization comparison
baseline_distance = 200.0
distance_saved = baseline_distance - optimized_distance
improvement = (distance_saved / baseline_distance) * 100

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="rw-header">
        <div class="rw-title">🚚 RouteWise</div>
        <div class="rw-subtitle">
            Smart Last-Mile Delivery Intelligence
            <br>
            Optimize routes. Predict delays. Take action.
        </div>
        <div class="status-badge">● SYSTEM ONLINE</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# KPI ROW
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div>📦</div>
            <div class="kpi-label">TOTAL ORDERS</div>
            <div class="kpi-value">{total_orders}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div>🚛</div>
            <div class="kpi-label">ACTIVE VEHICLES</div>
            <div class="kpi-value">{total_vehicles}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div>🛣️</div>
            <div class="kpi-label">OPTIMIZED DISTANCE</div>
            <div class="kpi-value">{optimized_distance:.1f} km</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div>🚨</div>
            <div class="kpi-label">HIGH-RISK DELIVERIES</div>
            <div class="kpi-value">{high_risk_deliveries}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# --------------------------------------------------
# ROUTE + FLEET STATUS
# --------------------------------------------------

left, right = st.columns([2.1, 1])

with left:
    st.markdown(
        '<div class="panel-title">🗺️ Route Intelligence</div>',
        unsafe_allow_html=True
    )

        # Get routes from the real optimizer
    if len(route_results) > 0:

        vehicle_options = [
            r["vehicle_id"]
            for r in route_results
        ]

        selected_vehicle = st.selectbox(
            "Select Vehicle",
            vehicle_options
        )

        selected_route = next(
            r for r in route_results
            if r["vehicle_id"] == selected_vehicle
        )

        route = selected_route["route"]
        # Remove consecutive duplicate Depot entries
        clean_route = []

        for point in route:
            if not clean_route or point != clean_route[-1]:
                clean_route.append(point)

        route = clean_route

        # Create locations from actual orders
        locations = {
            "Depot": (0, 0)
        }

        for _, row in orders_df.iterrows():
            locations[row["order_id"]] = (
                row["x"],
                row["y"]
            )

    else:
        st.warning("No optimized routes available.")
        route = ["Depot"]
        locations = {"Depot": (0, 0)}

    x_vals = []
    y_vals = []
    labels = []

    for point in route:

        if point == "Depot":
            x, y = 0, 0

        else:
            order = orders_df[
            orders_df["order_id"] == point
        ]

            if len(order) == 0:
                continue

            x = order.iloc[0]["x"]
            y = order.iloc[0]["y"]

        x_vals.append(x)
        y_vals.append(y)
        labels.append(point)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines+markers+text",
            text=labels,
            textposition="top center",
            line=dict(width=4),
            marker=dict(size=12),
            hovertemplate="<b>%{text}</b><extra></extra>"
        )
    )

    fig.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(
            title="Delivery Zone X",
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Delivery Zone Y",
            showgrid=True,
            zeroline=False
        ),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown(
        '<div class="panel-title">🚛 Fleet Status</div>',
        unsafe_allow_html=True
    )

    fleet = []

    for r in route_results:

        order_count = sum(
            1 for p in r["route"]
            if p != "Depot"
        )

        if order_count == 0:
            status = "⚪ Idle"
        else:
            status = "🟢 Active"

        fleet.append(
            (
                r["vehicle_id"],
                f"{order_count} orders assigned",
                status
            )
        )

    for name, detail, status in fleet:
        st.markdown(
            f"""
            <div class="vehicle-card">
                <div class="vehicle-name">{name}</div>
                <div class="vehicle-details">{detail}</div>
                <div class="vehicle-details">{status}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# PERFORMANCE + ATTENTION
# --------------------------------------------------

st.divider()

perf_col, alert_col = st.columns([1.25, 1])

with perf_col:
    st.markdown(
        '<div class="panel-title">📊 Route Performance</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Baseline", f"{baseline_distance:.1f} km")

    with m2:
        st.metric("Optimized", f"{optimized_distance:.1f} km")

    with m3:
        st.metric(
            "Improvement",
            f"{improvement:.1f}%",
            delta=f"-{distance_saved:.1f} km"
        )

    comparison_fig = go.Figure()

    comparison_fig.add_trace(
        go.Bar(
            x=["Baseline", "Optimized"],
            y=[baseline_distance, optimized_distance],
            text=[
                f"{baseline_distance:.1f} km",
                f"{optimized_distance:.1f} km"
            ],
            textposition="auto"
        )
    )

    comparison_fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Distance (km)",
        showlegend=False
    )

    st.plotly_chart(
        comparison_fig,
        use_container_width=True
    )

with alert_col:
    st.markdown(
        '<div class="panel-title">🚨 Attention Required</div>',
        unsafe_allow_html=True
    )

    # ============================================================
# REAL ATTENTION ALERTS
# ============================================================

    high_risk_orders = risk_df[
        risk_df["risk_level"] == "High"
    ].sort_values(
        "risk_score",
        ascending=False
    )

    critical_orders = critical_df[
        critical_df["critical"] == True
    ]

    exception_orders = exception_df[
        exception_df["exception"] == True
    ]

# High-risk delivery alerts
    for _, row in high_risk_orders.head(3).iterrows():
        st.error(
            f"🔴 {row['order_id']} — "
            f"High late-delivery risk: {row['risk_score']:.2f}"
    )

# Critical delivery alerts
    for _, row in critical_orders.head(2).iterrows():
        st.warning(
            f"⚠️ {row['order_id']} — "
            f"Critical delivery: {row['critical_reason']}"
    )

# Exception alerts
    for _, row in exception_orders.head(2).iterrows():
        st.warning(
            f"🚨 {row['order_id']} — "
            f"Exception: {row['exception_reason']}"
    )

# No issues
    if (
        len(high_risk_orders) == 0
        and len(critical_orders) == 0
        and len(exception_orders) == 0
    ):
        st.success("✅ No immediate attention required.")
# --------------------------------------------------
# RISK TABLE
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="panel-title">🚨 Delivery Risk Monitor</div>',
    unsafe_allow_html=True
)

# Use real risk prediction data
risk_display_df = risk_df.copy()

risk_display_df = risk_display_df.sort_values(
    "risk_score",
    ascending=False
)

risk_display_df = risk_display_df[
    [
        "order_id",
        "risk_score",
        "risk_level"
    ]
]

risk_display_df = risk_display_df.rename(
    columns={
        "order_id": "Order",
        "risk_score": "Risk Score",
        "risk_level": "Risk Level"
    }
)



st.dataframe(
    risk_display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score",
            min_value=0,
            max_value=100,
            format="%d"
        )
    }
)

# --------------------------------------------------
# RECOMMENDATION PANEL
# --------------------------------------------------

st.divider()

rec_col, summary_col = st.columns([1.4, 1])

with rec_col:
    st.markdown(
        '<div class="panel-title">💡 Recommended Action</div>',
        unsafe_allow_html=True
    )

    # ============================================================
# REAL RECOMMENDATION
# ============================================================

    if len(high_risk_orders) > 0:

        top_risk = high_risk_orders.iloc[0]

        st.info(
        f"🔴 Prioritize {top_risk['order_id']} before dispatch. "
        f"Risk score: {top_risk['risk_score']:.2f} "
        f"({top_risk['risk_level']} risk)."
    )

    elif len(exception_orders) > 0:

        top_exception = exception_orders.iloc[0]

        st.info(
        f"🚨 Review {top_exception['order_id']} before dispatch. "
        f"Reason: {top_exception['exception_reason']}."
    )

    elif len(critical_orders) > 0:

        top_critical = critical_orders.iloc[0]

        st.info(
        f"⚠️ Prioritize {top_critical['order_id']} "
        f"because it is a critical delivery. "
        f"Reason: {top_critical['critical_reason']}."
    )

    else:

        st.success(
        "✅ No immediate delivery action is required."
    )

with summary_col:
    st.markdown(
        '<div class="panel-title">📌 Optimization Summary</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"Route distance reduced by {distance_saved:.1f} km "
        f"({improvement:.1f}%) compared with the baseline."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.write("")
st.caption(
    "RouteWise • Last-Mile Delivery Optimization & Risk Intelligence"
)

st.caption(
    "RouteWise • Live project data from orders, vehicles, risk, and optimizer modules."
)