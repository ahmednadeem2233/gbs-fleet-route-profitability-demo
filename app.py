import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# =============================================================================
# GLOBAL BRIDGE SERVICES — CLIENT-FACING LOGISTICS INTELLIGENCE DEMO
# =============================================================================
st.set_page_config(
    page_title="GBS | Enterprise Fleet & Route Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# HIGH-CONTRAST PROFESSIONAL EXECUTIVE THEME
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg-main: #0b0f19;
    --card-bg: #111827;
    --border: #1f2937;
    --text-main: #f9fafb;
    --text-muted: #9ca3af;
    --accent-cyan: #38bdf8;
    --status-green: #10b981;
    --status-red: #ef4444;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-main) !important;
}

.stApp {
    background: var(--bg-main);
}

#MainMenu, footer, header, .stDeployButton {
    visibility: hidden;
    display: none;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1600px;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    min-width: 270px;
    max-width: 270px;
    background: #0d1322 !important;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--text-main) !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #ffffff !important;
    background-color: #172136 !important;
}

/* Multiselect Tag styling */
span[data-baseweb="tag"] {
    background-color: #1e293b !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 4px !important;
}

span[data-baseweb="tag"] * {
    color: #38bdf8 !important;
}

.sidebar-brand {
    padding: 10px 4px 18px 4px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 15px;
}

.sidebar-brand .mini {
    color: var(--accent-cyan) !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
}

.sidebar-brand .name {
    color: #ffffff !important;
    font-size: 18px;
    font-weight: 800;
    margin-top: 2px;
}

.sidebar-brand .desc {
    color: var(--text-muted) !important;
    font-size: 11px;
}

.control-title {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    margin: 18px 0 8px 0;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    border-radius: 12px;
    padding: 20px 24px;
    color: #0f172a;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    margin-bottom: 18px;
    border: 1px solid #ffffff;
}

.hero h1 {
    font-size: 24px;
    margin: 4px 0;
    color: #0f172a;
    font-weight: 800;
}

.demo-pill {
    background: #0f172a;
    border: 1px solid #1e293b;
    color: #38bdf8;
    border-radius: 999px;
    padding: 6px 14px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
}

/* KPI Cards */
.kpi {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

.kpi .label {
    color: var(--text-muted);
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.kpi .value {
    color: var(--text-main);
    font-size: 24px;
    font-weight: 800;
    margin-top: 4px;
}

.kpi .sub {
    font-size: 10px;
    color: var(--text-muted);
    margin-top: 4px;
}

.kpi .bad { color: var(--status-red); font-weight: 700; }
.kpi .good { color: var(--status-green); font-weight: 700; }

.action-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 10px;
}

/* CUSTOM TAB NAVIGATION */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #0d1322;
    padding: 6px;
    border: 1px solid var(--border);
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    height: 40px;
    border-radius: 8px;
    padding: 0 20px;
    background: transparent !important;
    color: var(--text-muted) !important;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid transparent !important;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background: #172136 !important;
}

.stTabs [aria-selected="true"] {
    background: #172136 !important;
    color: var(--accent-cyan) !important;
    border: 1px solid var(--accent-cyan) !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
}

.stTabs [aria-selected="true"] * {
    color: var(--accent-cyan) !important;
}

/* Footer */
.gbs-footer {
    border-top: 1px solid var(--border);
    margin-top: 30px;
    padding-top: 12px;
    color: var(--text-muted);
    font-size: 10px;
    display: flex;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="mini">GLOBAL BRIDGE SERVICES</div>
    <div class="name">Enterprise Intelligence</div>
    <div class="desc">Client Demonstration Portal</div>
</div>
<div class="control-title">Network & Operations</div>
""", unsafe_allow_html=True)

region = st.sidebar.selectbox(
    "Regional Hub",
    [
        "Midlands (DIRFT / Daventry)",
        "North West (Widnes / Multi-modal)",
        "Scotland & Borders (Carlisle)"
    ]
)

# Placeholder updated to 'All Fleet'
fleet_type = st.sidebar.multiselect(
    "Active Fleet Segment",
    ["Artic HGVs (44t)", "Rigids (18t)", "Electric Urban Vans"],
    default=["Artic HGVs (44t)", "Rigids (18t)"],
    placeholder="All Fleet"
)

st.sidebar.markdown('<div class="control-title">Financial Variables</div>', unsafe_allow_html=True)

spot_lease_cost = st.sidebar.slider("Spot Rental Rate (£/day)", 200, 500, 340, 10)
backhaul_efficiency = st.sidebar.slider("Target Backhaul Utilization (%)", 30, 95, 65, 5)
fuel_price_index = st.sidebar.slider("Fuel Surcharge Index (+/- %)", -15, 25, 5, 1)

st.sidebar.markdown("""
<div style="margin-top:20px;padding:12px;border:1px solid #1f2937;border-radius:8px;background:#172136;">
<div style="font-size:9px;color:#38bdf8;font-weight:800;letter-spacing:1px;">LIVE MODEL ENGINE</div>
<div style="font-size:11px;color:#ffffff;margin-top:3px;font-weight:600;">Connected to 48 Depots</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# DYNAMIC SIMULATION LOGIC
# =============================================================================
seed = sum(ord(c) for c in region) + len(fleet_type) * 10
np.random.seed(seed)

days = [f"Day {i+1}" for i in range(14)]
base_owned = 500 if "Artic HGVs (44t)" in fleet_type else 350
demand = (np.array([420, 440, 480, 520, 610, 660, 620, 430, 450, 490, 540, 630, 690, 640]) + np.random.randint(-30, 40, 14)).tolist()

df_cap = pd.DataFrame({"Day": days, "Demand": demand, "Owned": [base_owned]*14})
df_cap["Deficit"] = (df_cap["Demand"] - df_cap["Owned"]).clip(lower=0)

# Total Truck-Days Calculation
total_truck_days = int(df_cap["Deficit"].sum())
total_lease = total_truck_days * spot_lease_cost
peak_gap = int(df_cap["Deficit"].max())

routes = ["London RDC Corridor", "Manchester Freight Hub", "Birmingham Apex", "Glasgow Distribution"]
revenue = np.random.randint(900, 1500, 4)
fuel = np.random.randint(250, 500, 4) * (1 + fuel_price_index/100)
drivers = np.random.randint(200, 400, 4)
backhaul_leakage = [int(320 * (1 - backhaul_efficiency/100)) for _ in range(4)]

df_routes = pd.DataFrame({
    "Route": routes,
    "Revenue": revenue,
    "Fuel & Tolls": fuel,
    "Driver Cost": drivers,
    "Empty Leakage": backhaul_leakage
})
df_routes["Total Cost"] = df_routes["Fuel & Tolls"] + df_routes["Driver Cost"] + df_routes["Empty Leakage"]
df_routes["Net Profit"] = df_routes["Revenue"] - df_routes["Total Cost"]
df_routes["Margin %"] = (df_routes["Net Profit"] / df_routes["Revenue"] * 100).round(1)

# =============================================================================
# HERO SECTION
# =============================================================================
st.markdown("""
<div class="hero">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="color:#0284c7;font-size:10px;font-weight:800;letter-spacing:1.5px;">GLOBAL BRIDGE SERVICES · NETWORK ANALYTICS</div>
            <h1>Fleet & Route Profitability Command Center</h1>
            <div style="color:#475569;font-size:11px;font-weight:600;">Predictive capacity planning · True Cost-to-Serve audit · Commercial recovery Engine</div>
        </div>
        <div class="demo-pill">EDDIE STOBART DEMO ENVIRONMENT</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# TOP KPI METRICS STRIP (Updated Precise Labels)
# =============================================================================
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="kpi"><div class="label">Projected Spot-Lease Exposure</div><div class="value">£{total_lease:,.0f}</div><div class="sub bad">({total_truck_days:,} truck-days × £{spot_lease_cost})</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi"><div class="label">Peak Capacity Gap</div><div class="value">{peak_gap} Units</div><div class="sub bad">High Risk on Peak Days</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi"><div class="label">Emergency Capacity Exposure</div><div class="value">{total_truck_days:,} Truck-Days</div><div class="sub">14-day cumulative shortage</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="kpi"><div class="label">Avg Backhaul Opportunity</div><div class="value">£{int(df_routes["Empty Leakage"].mean()):,.0f}/run</div><div class="sub good">▲ Opportunity Identified</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="kpi"><div class="label">Network Efficiency</div><div class="value">{82 - fuel_price_index/2:.1f}%</div><div class="sub good">Target: 85.0%</div></div>', unsafe_allow_html=True)

st.write("")

# =============================================================================
# WORKFLOW TABS
# =============================================================================
t1, t2, t3, t4 = st.tabs([
    "01  Capacity & Demand Forecast",
    "02  True Cost-To-Serve Audit",
    "03  Utilization Heatmap",
    "04  Commercial Executive Summary"
])

# -----------------------------------------------------------------------------
# TAB 1: DEMAND & CAPACITY
# -----------------------------------------------------------------------------
with t1:
    st.subheader(f"14-Day Demand vs Available Fleet ({region})")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_cap["Day"], y=df_cap["Demand"], name="Forecasted Demand", line=dict(color="#38bdf8", width=3)))
    fig.add_trace(go.Scatter(x=df_cap["Day"], y=df_cap["Owned"], name="Owned Fleet", line=dict(color="#9ca3af", width=2, dash="dash")))
    fig.add_trace(go.Bar(x=df_cap["Day"], y=df_cap["Deficit"], name="Shortage Gap", marker_color="#ef4444", opacity=0.5))
    
    fig.update_layout(
        height=300,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Plus Jakarta Sans"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.1, x=0),
        yaxis=dict(gridcolor="#1f2937"),
        xaxis=dict(gridcolor="#1f2937")
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="action-card">
            <h4 style="margin:0;color:#38bdf8;">Peak Deficit Analysis</h4>
            <p style="font-size:12px;color:#9ca3af;margin-top:6px;line-height:1.6;">
            The network faces a peak deficit of <b style="color:#ffffff;">{peak_gap} vehicles</b>. Spot renting at £{spot_lease_cost}/day creates <b style="color:#ffffff;">£{total_lease:,.0f}</b> in financial exposure across <b style="color:#ffffff;">{total_truck_days:,} truck-days</b> of cumulative shortage.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="action-card">
            <h4 style="margin:0;color:#10b981;">Optimization Strategy</h4>
            <p style="font-size:12px;color:#9ca3af;margin-top:6px;line-height:1.6;">
            Inter-depot positioning from lower-demand hubs can offset up to <b style="color:#ffffff;">65% of spot rental costs</b> if transfers are initiated 48 hours ahead of the peak curve.
            </p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: ROUTE PROFITABILITY
# -----------------------------------------------------------------------------
with t2:
    st.subheader(f"Route-Level Cost-to-Serve Breakdowns ({region})")
    
    formatted_df = df_routes.copy()
    formatted_df["Revenue"] = formatted_df["Revenue"].map(lambda x: f"£{x:,.0f}")
    formatted_df["Total Cost"] = formatted_df["Total Cost"].map(lambda x: f"£{x:,.0f}")
    formatted_df["Net Profit"] = formatted_df["Net Profit"].map(lambda x: f"£{x:,.0f}")
    formatted_df["Margin %"] = formatted_df["Margin %"].map(lambda x: f"{x}%")
    st.dataframe(formatted_df, use_container_width=True, hide_index=True)

    fig2 = px.bar(
        df_routes,
        x="Route",
        y=["Fuel & Tolls", "Driver Cost", "Empty Leakage", "Net Profit"],
        title="Cost Structure vs Profitability per Run",
        barmode="stack",
        color_discrete_sequence=["#ef4444", "#f59e0b", "#3b82f6", "#10b981"]
    )
    fig2.update_layout(
        height=280,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Plus Jakarta Sans"),
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(gridcolor="#1f2937"),
        xaxis=dict(gridcolor="#1f2937")
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# TAB 3: HEATMAP ANALYTICS
# -----------------------------------------------------------------------------
with t3:
    st.subheader("Depot Fleet Utilization Heatmap (24-Hour Operating Window)")
    
    hours = [f"{h:02d}:00" for h in range(0, 24, 2)]
    depots = ["Daventry Hub", "DIRFT Terminal", "Widnes Logistics", "Carlisle Depot", "Glasgow South"]
    heatmap_data = np.random.randint(55, 99, size=(len(depots), len(hours)))

    fig3 = px.imshow(
        heatmap_data,
        labels=dict(x="Time of Day", y="Operating Depot", color="Utilization %"),
        x=hours,
        y=depots,
        color_continuous_scale="Blues"
    )
    fig3.update_layout(
        height=290,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#9ca3af", family="Plus Jakarta Sans"),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# TAB 4: EXECUTIVE SUMMARY & EXPORT
# -----------------------------------------------------------------------------
with t4:
    st.subheader("Commercial Action Simulator & Executive Exports")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background:#111827;padding:18px;border-radius:10px;border:1px solid #1f2937;">
            <h3 style="color:#38bdf8;margin-top:0;font-size:16px;">Key Executive Deliverables</h3>
            <ul style="color:#d1d5db;font-size:12px;line-height:1.9;padding-left:18px;">
                <li><b style="color:#ffffff;">Backhaul Optimization:</b> Capturing dynamic return loads reduces network leakages by up to £1.2M annually.</li>
                <li><b style="color:#ffffff;">Dynamic Pricing Surcharges:</b> Implementing automated Clean Air Zone (CAZ) pass-through fees protects route margins against regulatory creep.</li>
                <li><b style="color:#ffffff;">Predictive Spot Lease Lock-in:</b> Forward booking spot capacity during predicted peak windows yields 18% lower daily rental charges.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div style="background:#111827;padding:18px;border-radius:10px;border:1px solid #1f2937;">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0;color:#ffffff;font-size:14px;'>Export Audit Package</h4>", unsafe_allow_html=True)
        st.write("")
        st.button("📄 Download Full PDF Audit", use_container_width=True)
        st.button("📊 Export Raw Datasets (CSV)", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div class="gbs-footer">
    <span>GLOBAL BRIDGE SERVICES · Logistics & Fleet Intelligence Engine</span>
    <span>Confidential Presentation · Simulated Client Operational Data</span>
</div>
""", unsafe_allow_html=True)