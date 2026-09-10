import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="RouteWise",
    page_icon="🚚",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🚚 RouteWise")

st.subheader(
    "Last-Mile Delivery Route Optimizer & Late-Delivery Risk Predictor"
)

st.write(
    "A smart dashboard for optimizing delivery routes "
    "and identifying late-delivery risks."
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.divider()

st.header("📌 Delivery Overview")

# Dummy values for dashboard development
total_orders = 30
total_vehicles = 4
optimized_distance = 36.2
high_risk_deliveries = 2

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        total_orders
    )

with col2:
    st.metric(
        "Vehicles",
        total_vehicles
    )

with col3:
    st.metric(
        "Optimized Distance",
        f"{optimized_distance:.1f} km"
    )

with col4:
    st.metric(
        "High-Risk Deliveries",
        high_risk_deliveries
    )

# --------------------------------------------------
# BASELINE VS OPTIMIZED
# --------------------------------------------------

st.divider()

st.header("📊 Baseline vs Optimized")

# Dummy values for dashboard development
baseline_distance = 50.0
optimized_distance = 36.2

distance_saved = baseline_distance - optimized_distance

improvement = (
    distance_saved / baseline_distance
) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Baseline Distance",
        f"{baseline_distance:.1f} km"
    )

with col2:
    st.metric(
        "Optimized Distance",
        f"{optimized_distance:.1f} km"
    )

with col3:
    st.metric(
        "Distance Improvement",
        f"{improvement:.1f}%"
    )

# --------------------------------------------------
# CURRENT STATUS
# --------------------------------------------------

st.divider()

st.header("🚦 Current Status")

st.success(
    "Routes are currently being displayed using sample data."
)

st.info(
    "Optimization and risk prediction results will be connected "
    "after integrating Member 1 and Member 2 modules."
)