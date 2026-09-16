import streamlit as st
from html import escape

st.set_page_config(
    page_title="GBS — True Cost Per Mile Dashboard",
    page_icon="GBS",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Demo data / editable controls
# -----------------------------
if "prospect_name" not in st.session_state:
    st.session_state.prospect_name = "Girteka Logistics"

if "current_cost" not in st.session_state:
    st.session_state.current_cost = 1.92

if "optimized_cost" not in st.session_state:
    st.session_state.optimized_cost = 1.54

if "annual_impact" not in st.session_state:
    st.session_state.annual_impact = 186400

trucks = [
    ("GBS-104", 1.99),
    ("GBS-107", 1.88),
    ("GBS-102", 1.59),
    ("GBS-101", 1.56),
    ("GBS-103", 1.54),
    ("GBS-105", 1.47),
    ("GBS-108", 1.45),
    ("GBS-106", 1.42),
]

routes = [
    ("Newark, NJ → Columbus, OH", 1.99),
    ("Charlotte, NC → Chicago, IL", 1.88),
    ("LA, CA → Phoenix, AZ", 1.59),
    ("Chicago, IL → Dallas, TX", 1.56),
    ("Atlanta, GA → Miami, FL", 1.54),
    ("Seattle, WA → Denver, CO", 1.47),
    ("Denver, CO → Kansas City, MO", 1.45),
    ("Houston, TX → Memphis, TN", 1.42),
]

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
    :root {
        --bg: #050b13;
        --panel: #0a1420;
        --panel2: #0e1b2a;
        --line: #1d3348;
        --line2: #294963;
        --text: #f5f8fb;
        --muted: #8da1b4;
        --blue: #2f9cf4;
        --cyan: #73d8ff;
        --green: #5bd7a2;
        --red: #ff6b72;
        --yellow: #e8bd57;
    }

    .stApp {
        background:
            radial-gradient(circle at 80% 0%, rgba(35, 112, 174, .12), transparent 25%),
            radial-gradient(circle at 20% 100%, rgba(20, 72, 115, .10), transparent 30%),
            #050b13;
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(5, 11, 19, .98);
        border-bottom: 1px solid rgba(53, 83, 108, .35);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050c15 0%, #07121d 100%);
        border-right: 1px solid #193047;
    }

    [data-testid="stSidebar"] * { color: #e8eff5; }

    .block-container {
        max-width: 1480px;
        padding-top: 1.35rem;
        padding-bottom: 3rem;
    }

    .brand {
        display:flex;
        align-items:center;
        gap:12px;
        margin: 5px 0 27px;
    }

    .brand-logo {
        width:40px;height:40px;border-radius:11px;
        background:linear-gradient(145deg,#2fa8ff,#126fba);
        display:flex;align-items:center;justify-content:center;
        font-weight:900;color:white;font-size:13px;
        box-shadow:0 8px 28px rgba(26,145,224,.22);
        border:1px solid rgba(255,255,255,.10);
    }

    .brand-name {
        font-size:17px;
        line-height:1.05;
        font-weight:800;
        letter-spacing:-.25px;
    }

    .side-foot {
        position: fixed;
        bottom: 18px;
        width: 245px;
        color:#74899c;
        font-size:10px;
        line-height:1.55;
        border-top:1px solid #193047;
        padding-top:13px;
    }

    .topline {
        color:#78b7dc;
        font-size:11px;
        letter-spacing:.55px;
        margin-bottom:17px;
        text-transform:uppercase;
    }

    .warning {
        float:right;
        border:1px solid rgba(221,177,78,.75);
        color:#e9c260;
        border-radius:7px;
        padding:7px 12px;
        font-size:9px;
        letter-spacing:1.05px;
        font-weight:800;
        background:rgba(91,67,17,.10);
    }

    .hero {
        border:1px solid #244159;
        border-radius:15px;
        padding:29px 31px 25px;
        background:
            radial-gradient(circle at 92% 8%, rgba(40,139,215,.17), transparent 28%),
            linear-gradient(145deg,#0d2133 0%,#091521 70%);
        margin-bottom:17px;
        box-shadow:0 18px 55px rgba(0,0,0,.22);
    }

    .hero h1 {
        font-size:36px;
        margin:0 0 7px;
        font-weight:850;
        letter-spacing:-1.35px;
        color:#f7fafc;
    }

    .hero p {
        color:#9eb1c1;
        margin:0;
        font-size:13px;
        line-height:1.55;
    }

    .prepared {
        margin-top:20px;
        display:flex;
        align-items:center;
        gap:12px;
        color:#7f96aa;
        font-size:12px;
    }

    .prospect {
        background:#12263a;
        border:1px solid #31506a;
        color:#f4f8fb;
        border-radius:7px;
        padding:8px 13px;
        font-weight:750;
        box-shadow:inset 0 1px rgba(255,255,255,.035);
    }

    .flow {
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:8px;
        margin-top:22px;
    }

    .flow-item {
        background:rgba(17,38,57,.72);
        border:1px solid #29465f;
        border-radius:8px;
        padding:12px;
        text-align:center;
        font-size:11px;
        color:#dbe7ef;
    }

    .flow-item b { color:#fff; display:block; margin-bottom:3px; }
    .flow-item span { color:#7893a8; font-size:9px; }

    .kpi {
        background:linear-gradient(145deg,#0c1b2a,#091521);
        border:1px solid #263f56;
        border-radius:12px;
        padding:20px;
        min-height:125px;
        box-shadow:0 12px 34px rgba(0,0,0,.16);
    }

    .kpi-label { color:#8da4b7; font-size:11px; letter-spacing:.1px; }
    .kpi-value { color:#f8fafc; font-size:30px; font-weight:850; margin:8px 0 4px; letter-spacing:-.7px; }
    .kpi-sub { color:#6f879b; font-size:10px; }
    .kpi-green .kpi-value { color:#67dfaa; }

    .section-title {
        font-size:13px;
        font-weight:800;
        color:#e9f0f5;
        margin:25px 0 9px;
        letter-spacing:.1px;
    }

    .card {
        background:linear-gradient(145deg,#0b1927,#091520);
        border:1px solid #263f56;
        border-radius:11px;
        padding:18px;
        box-shadow:0 10px 30px rgba(0,0,0,.13);
    }

    .bar-row {
        display:grid;
        grid-template-columns:180px 1fr 55px;
        gap:10px;
        align-items:center;
        margin:9px 0;
        font-size:11px;
    }

    .bar-bg {
        height:8px;
        background:#182c40;
        border-radius:20px;
        overflow:hidden;
    }

    .bar-fill {
        height:100%;
        border-radius:20px;
        background:linear-gradient(90deg,#218ee4,#5bcfff);
        box-shadow:0 0 10px rgba(65,181,245,.16);
    }

    .bar-fill.red { background:#e85d68; box-shadow:none; }
    .bar-fill.green { background:#50ce98; box-shadow:none; }

    .insight {
        border:1px solid #263f56;
        border-radius:9px;
        padding:13px 15px;
        margin:8px 0;
        background:#0b1a29;
        font-size:11px;
        color:#dbe6ee;
    }

    .insight .tag {
        color:#69cfff;
        font-weight:800;
        margin-right:8px;
    }

    .cta {
        background:linear-gradient(120deg,#0d2439,#091725);
        border:1px solid #2b4b66;
        border-radius:11px;
        padding:21px;
        margin-top:20px;
        box-shadow:0 14px 35px rgba(0,0,0,.18);
    }

    .cta h3 { margin:0 0 7px; font-size:18px; }
    .cta p { color:#91a8ba; font-size:11px; margin:0; }

    .footer {
        color:#647c90;
        font-size:9px;
        border-top:1px solid #1b344a;
        padding-top:13px;
        margin-top:28px;
        display:flex;
        justify-content:space-between;
        letter-spacing:.15px;
    }

    .small-note,.page-note {
        color:#70889c;
        font-size:10px;
        margin-bottom:14px;
    }

    .stButton > button {
        background:linear-gradient(135deg,#198fe2,#126eb4);
        color:white;
        border:1px solid rgba(117,211,255,.22);
        border-radius:7px;
        font-weight:800;
        box-shadow:0 7px 20px rgba(20,117,181,.18);
    }

    .stButton > button:hover {
        background:linear-gradient(135deg,#2aa5f4,#1781ca);
        color:white;
        border-color:rgba(117,211,255,.35);
    }

    div[data-baseweb="input"] {
        background:#0e2132;
        border:1px solid #27445c;
        border-radius:7px;
    }

    input { color:white !important; }

    [data-testid="stExpander"] {
        border:1px solid #203a51;
        border-radius:9px;
        background:#091521;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-logo">GBS</div>
        <div class="brand-name">Global Bridge<br>Services</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Cost & Fuel Analytics",
            "Fleet & Routes",
            "Maintenance Tracking",
            "Data Integration",
            "Reports",
        ],
        label_visibility="collapsed",
    )


    st.markdown("""
    <div class="side-foot">
        <b>Demo environment.</b><br>
        All figures are illustrative sample data.<br><br>
        GBS — True Cost Per Mile Dashboard
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="topline">AI-powered logistics analytics, applied to fleet cost '
    '<span class="warning">● ILLUSTRATIVE SAMPLE DATA — NOT ACTUAL CLIENT NUMBERS</span></div>',
    unsafe_allow_html=True
)

# -----------------------------
# Executive Overview
# -----------------------------
if page == "Executive Overview":
    st.markdown(f"""
    <div class="hero">
        <h1>True Cost Per Mile — By Truck &amp; Route</h1>
        <p>Fuel, driver pay, maintenance, and tolls — unified into one number your ops team<br>
        can act on every morning.</p>
        <div class="prepared">
            <span>Prepared for</span>
            <span class="prospect">{escape(st.session_state.prospect_name)}</span>
        </div>
        <div class="flow">
            <div class="flow-item"><b>Fuel</b><span>Fuel card / purchases</span></div>
            <div class="flow-item"><b>Driver Pay</b><span>Payroll / driver cost</span></div>
            <div class="flow-item"><b>Maintenance</b><span>Service &amp; repairs</span></div>
            <div class="flow-item"><b>Tolls</b><span>Tolls &amp; fees</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">Current fleet average cost per mile</div>
            <div class="kpi-value">€{st.session_state.current_cost:.2f}<span style="font-size:14px"> / mi</span></div>
            <div class="kpi-sub">Across 8 active trucks · last 30 days · illustrative sample</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        reduction = (1 - st.session_state.optimized_cost / st.session_state.current_cost) * 100
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">Optimized cost / mile</div>
            <div class="kpi-value">€{st.session_state.optimized_cost:.2f}</div>
            <div class="kpi-sub">↓ {reduction:.0f}% projected improvement</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi kpi-green">
            <div class="kpi-label">Estimated annual impact</div>
            <div class="kpi-value">€{st.session_state.annual_impact:,.0f}</div>
            <div class="kpi-sub">Projected from flagged inefficiencies</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Current vs. optimized cost</div>', unsafe_allow_html=True)
    a,b,c = st.columns([1,1,1])
    with a:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div class="kpi-label">Current cost / mile</div>
            <div class="kpi-value">€{st.session_state.current_cost:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div class="kpi-label">Optimized cost / mile</div>
            <div class="kpi-value">€{st.session_state.optimized_cost:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with c:
        st.markdown(f"""
        <div class="card" style="text-align:center;border-color:#3f9674">
            <div class="kpi-label">Estimated annual impact</div>
            <div class="kpi-value" style="color:#67dda9">€{st.session_state.annual_impact:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Where the cost is coming from</div>', unsafe_allow_html=True)
    left,right = st.columns(2)
    with left:
        st.markdown('<div class="card"><b>Cost per mile, by truck</b>', unsafe_allow_html=True)
        maxv = max(v for _,v in trucks)
        for name,val in trucks:
            cls = "red" if val >= 1.88 else ""
            pct = val/maxv*100
            st.markdown(f"""
            <div class="bar-row"><span>{name}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{pct:.1f}%"></div></div>
            <span>€{val:.2f}</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><b>Cost per mile, by route</b>', unsafe_allow_html=True)
        maxv = max(v for _,v in routes)
        for name,val in routes:
            short = name.replace(" → ", " → ")
            pct = val/maxv*100
            cls = "red" if val >= 1.88 else ""
            st.markdown(f"""
            <div class="bar-row"><span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{short}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{pct:.1f}%"></div></div>
            <span>€{val:.2f}</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="cta">
        <h3>See what your fleet is actually costing you.</h3>
        <p>Built on your own fuel, payroll, maintenance, and toll data — with a focused view of true cost per mile.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Cost & Fuel Analytics
# -----------------------------
elif page == "Cost & Fuel Analytics":
    st.markdown("## Cost & Fuel Analytics")
    st.markdown('<div class="page-note">Illustrative sample data — use this view to identify where cost-per-mile is coming from.</div>', unsafe_allow_html=True)

    left,right = st.columns(2)
    with left:
        st.markdown('<div class="card"><b>Cost per mile, by truck</b>', unsafe_allow_html=True)
        maxv = max(v for _,v in trucks)
        for name,val in trucks:
            cls = "red" if val >= 1.88 else ""
            st.markdown(f"""
            <div class="bar-row"><span>{name}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{val/maxv*100:.1f}%"></div></div>
            <span>€{val:.2f}</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><b>Fuel spend composition</b>', unsafe_allow_html=True)
        fuel = [("Diesel purchases",71,""),("Idle-time burn",14,""),("Route detour overhead",9,"red"),("Off-route fuel stops",6,"")]
        for name,val,cls in fuel:
            st.markdown(f"""
            <div class="bar-row"><span>{name}</span>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{val}%"></div></div>
            <span>{val}%</span></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Cost breakdown — fleet average, per mile</div>', unsafe_allow_html=True)
    components = [("Fuel",.64),("Driver pay",.67),("Maintenance",.29),("Tolls & fees",.10)]
    total = sum(v for _,v in components)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for name,val in components:
        st.markdown(f"""
        <div class="bar-row">
            <span>{name}</span>
            <div class="bar-bg"><div class="bar-fill" style="width:{val/max(v for _,v in components)*100:.1f}%"></div></div>
            <span>€{val:.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Flagged insights</div>', unsafe_allow_html=True)
    for tag,text in [
        ("⚠", "GBS-104 — maintenance cost running 22% above fleet average. Service overdue."),
        ("⛽", "Chicago → Dallas route shows 6% recoverable fuel efficiency vs. benchmark."),
        ("▣", "Projected 12% further savings available through route consolidation on low-utilization lanes."),
    ]:
        st.markdown(f'<div class="insight"><span class="tag">{tag}</span>{text}</div>', unsafe_allow_html=True)

# -----------------------------
# Fleet & Routes
# -----------------------------
elif page == "Fleet & Routes":
    st.markdown("## Fleet & Routes")
    st.markdown('<div class="page-note">Illustrative fleet view. Status flags highlight where attention may be required.</div>', unsafe_allow_html=True)

    rows = [
        ("GBS-101","Chicago, IL → Dallas, TX","88%","On target"),
        ("GBS-102","LA, CA → Phoenix, AZ","91%","On target"),
        ("GBS-104","Newark, NJ → Columbus, OH","62%","Needs attention"),
        ("GBS-106","Houston, TX → Memphis, TN","85%","On target"),
        ("GBS-107","Charlotte, NC → Chicago, IL","78%","Watch"),
    ]

    left,right = st.columns([1.15,1])
    with left:
        st.markdown('<div class="card"><b>Truck / Route / Utilization</b>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:grid;grid-template-columns:90px 1fr 70px 120px;gap:10px;color:#7590a4;font-size:10px;margin:13px 0">
        <span>Truck</span><span>Route</span><span>Utilization</span><span>Status</span></div>
        """, unsafe_allow_html=True)
        for t,r,u,s in rows:
            col = "#57dc9f" if s=="On target" else "#ffd34d" if s=="Watch" else "#ff656d"
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:90px 1fr 70px 120px;gap:10px;
            padding:12px 0;border-top:1px solid #1e354b;font-size:11px">
            <span>{t}</span><span>{r}</span><span>{u}</span><b style="color:{col}">{s}</b></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="card" style="height:100%">
            <b>Route network overview</b>
            <div style="height:260px;position:relative;margin-top:20px">
                <div style="position:absolute;left:12%;bottom:15%;width:12px;height:12px;background:#1da7ff;border-radius:50%"></div>
                <div style="position:absolute;left:34%;bottom:25%;width:12px;height:12px;background:#1da7ff;border-radius:50%"></div>
                <div style="position:absolute;right:20%;top:24%;width:13px;height:13px;background:#53d89a;border-radius:50%"></div>
                <div style="position:absolute;right:10%;bottom:35%;width:13px;height:13px;background:#53d89a;border-radius:50%"></div>
                <svg width="100%" height="100%" style="position:absolute;inset:0">
                    <line x1="17%" y1="78%" x2="80%" y2="31%" stroke="#3a7ea7" stroke-width="2" stroke-dasharray="5 5"/>
                    <line x1="39%" y1="68%" x2="80%" y2="31%" stroke="#3a7ea7" stroke-width="2" stroke-dasharray="5 5"/>
                    <line x1="39%" y1="68%" x2="90%" y2="60%" stroke="#3a7ea7" stroke-width="2" stroke-dasharray="5 5"/>
                </svg>
                <span style="position:absolute;left:8%;bottom:7%;color:#7894a9;font-size:10px">Origin A</span>
                <span style="position:absolute;left:28%;bottom:15%;color:#7894a9;font-size:10px">Origin B</span>
                <span style="position:absolute;right:12%;top:17%;color:#7894a9;font-size:10px">Dest. A</span>
                <span style="position:absolute;right:2%;bottom:27%;color:#7894a9;font-size:10px">Dest. B</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Maintenance
# -----------------------------
elif page == "Maintenance Tracking":
    st.markdown("## Maintenance Tracking")
    st.markdown('<div class="page-note">Illustrative maintenance status and upcoming service view.</div>', unsafe_allow_html=True)
    items = [
        ("⚠", "GBS-104 — service overdue by 9 days. Maintenance cost running 22% above fleet average.", "#ff656d"),
        ("↗", "GBS-107 — brake inspection due in 400 miles.", "#d8e7f2"),
        ("✓", "GBS-101, GBS-102, GBS-106 — up to date, no action needed.", "#55d89a"),
        ("▣", "3 scheduled services in the next 14 days across the fleet.", "#ffd34d"),
    ]
    for icon,text,col in items:
        st.markdown(f"""
        <div class="insight" style="padding:18px">
            <span style="color:{col};font-size:17px;margin-right:13px">{icon}</span>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Data Integration
# -----------------------------
elif page == "Data Integration":
    st.markdown("## Data Integration")
    st.markdown('<div class="page-note">Illustrative source-system connection status.</div>', unsafe_allow_html=True)
    integrations = [
        ("Fuel card provider","Connected",100,"green"),
        ("Dispatch / TMS system","Connected",100,"green"),
        ("Payroll / driver pay","Connected",100,"green"),
        ("Maintenance log system","In progress",62,""),
    ]
    for name,status,pct,cls in integrations:
        st.markdown(f"""
        <div class="card" style="margin-bottom:9px;padding:14px 17px">
            <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:8px">
                <b>{name}</b><span style="color:{'#58dda0' if status=='Connected' else '#ffd34d'}">{status}</span>
            </div>
            <div class="bar-bg"><div class="bar-fill {cls}" style="width:{pct}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Reports
# -----------------------------
elif page == "Reports":
    st.markdown("## Reports")
    st.markdown('<div class="page-note">Illustrative report catalogue.</div>', unsafe_allow_html=True)
    reports = [
        "Monthly Cost-per-Mile Summary — PDF, auto-generated on the 1st of each month.",
        "Fleet Efficiency Scorecard — per-truck breakdown, exportable to Excel.",
        "Maintenance Forecast Report — upcoming service needs by vehicle.",
    ]
    for text in reports:
        st.markdown(f'<div class="insight"><span style="color:#d8e7f2;margin-right:12px">□</span>{text}</div>', unsafe_allow_html=True)

# -----------------------------
# Reusable editor at bottom
# -----------------------------
with st.expander("GBS Demo Controls — edit prospect & sample figures"):
    col1,col2,col3 = st.columns(3)
    with col1:
        st.session_state.current_cost = st.number_input(
            "Current €/mile", min_value=0.01, value=float(st.session_state.current_cost), step=0.01
        )
    with col2:
        st.session_state.optimized_cost = st.number_input(
            "Optimized €/mile", min_value=0.01, value=float(st.session_state.optimized_cost), step=0.01
        )
    with col3:
        st.session_state.annual_impact = st.number_input(
            "Annual impact €", min_value=0, value=int(st.session_state.annual_impact), step=1000
        )

st.markdown(f"""
<div class="footer">
    <span>Confidential — prepared for {escape(st.session_state.prospect_name)} · Global Bridge Services (GBS)</span>
    <span>INTEGRATE · ANALYZE · OPTIMIZE · GROW</span>
</div>
""", unsafe_allow_html=True)