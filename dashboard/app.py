import streamlit as st
import plotly.graph_objects as go
import pandas as pd

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
        color: #6b7280;
        margin-top: 5px;
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
        color: #111827;
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

# --------------------------------------------------
# DUMMY DATA
# --------------------------------------------------

total_orders = 30
total_vehicles = 4
baseline_distance = 50.0
optimized_distance = 36.2
high_risk_deliveries = 2

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

    locations = {
        "Depot": (0, 0),
        "Order 1": (2, 3),
        "Order 2": (5, 2),
        "Order 3": (7, 5),
        "Order 4": (4, 7),
    }

    route = [
        "Depot",
        "Order 1",
        "Order 2",
        "Order 3",
        "Order 4",
        "Depot"
    ]

    x_vals = []
    y_vals = []
    labels = []

    for point in route:
        x, y = locations[point]
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

    fleet = [
        ("Vehicle 1", "2 orders assigned", "🟢 Active"),
        ("Vehicle 2", "1 order assigned", "🟠 Near capacity"),
        ("Vehicle 3", "1 order assigned", "🟢 Active"),
        ("Vehicle 4", "No orders assigned", "⚪ Idle"),
    ]

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

    st.error("🔴 Order 3 — High late-delivery risk: 91")
    st.warning("🟠 Order 2 — Medium late-delivery risk: 72")
    st.warning("⚠️ Vehicle 2 is approaching capacity limit")
    st.warning("⏰ Order 2 delivery window may be at risk")

# --------------------------------------------------
# RISK TABLE
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="panel-title">🚨 Delivery Risk Monitor</div>',
    unsafe_allow_html=True
)

risk_df = pd.DataFrame(
    {
        "Order": [
            "Order 3",
            "Order 2",
            "Order 4",
            "Order 1"
        ],
        "Vehicle": [
            "Vehicle 2",
            "Vehicle 1",
            "Vehicle 3",
            "Vehicle 1"
        ],
        "Risk Score": [
            91,
            72,
            45,
            25
        ],
        "Risk Level": [
            "High",
            "Medium",
            "Medium",
            "Low"
        ]
    }
)

st.dataframe(
    risk_df,
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

    st.info(
        "Prioritize Order 3 before dispatch. "
        "Review Vehicle 2 capacity and monitor Order 2's "
        "delivery window closely."
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
    "Dashboard currently uses sample data for UI development."
)