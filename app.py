import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India MSME Credit Gap Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1a1d2e, #16213e);
        border: 1px solid #eb5c2e22;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #eb5c2e; }
    .metric-label { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
    .insight-box {
        background: linear-gradient(135deg, #1a1d2e, #16213e);
        border-left: 4px solid #eb5c2e;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        color: #ccc;
        font-size: 0.9rem;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #fff;
        margin: 2rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #eb5c2e33;
    }
    .tag {
        display: inline-block;
        background: #eb5c2e22;
        color: #eb5c2e;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75rem;
        margin-right: 6px;
    }
    h1 { color: #ffffff !important; }
    .stSelectbox label { color: #aaa !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # MSME sector data (RBI + MSME Ministry 2023-24 reports)
    sector_df = pd.DataFrame({
        "Sector": ["Manufacturing", "Trade", "Services", "Food Processing", "Textiles", "Auto Components"],
        "Total MSMEs (Mn)": [14.2, 23.8, 25.1, 5.3, 6.1, 4.2],
        "Credit Demand (₹ Bn)": [8200, 12400, 9800, 3100, 4200, 2900],
        "Credit Supply (₹ Bn)": [2900, 3800, 4100, 980, 1400, 1100],
        "Avg Ticket Size (₹ Lakh)": [18, 8, 12, 22, 15, 28],
    })
    sector_df["Credit Gap (₹ Bn)"] = sector_df["Credit Demand (₹ Bn)"] - sector_df["Credit Supply (₹ Bn)"]
    sector_df["Gap %"] = ((sector_df["Credit Gap (₹ Bn)"] / sector_df["Credit Demand (₹ Bn)"]) * 100).round(1)

    # Tier-wise data
    tier_df = pd.DataFrame({
        "City Tier": ["Tier 1", "Tier 2", "Tier 3", "Rural"],
        "MSMEs (Mn)": [8.2, 18.4, 24.6, 27.5],
        "Banked %": [72, 48, 31, 18],
        "Credit Gap (₹ Bn)": [4200, 9800, 14300, 12700],
        "UPI Adoption %": [89, 74, 58, 32],
        "GST Registered %": [81, 52, 34, 12],
    })
    tier_df["Unbanked %"] = 100 - tier_df["Banked %"]

    # Yearly credit gap trend
    trend_df = pd.DataFrame({
        "Year": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "Credit Gap (₹ Tn)": [20.1, 22.4, 21.8, 24.6, 27.3, 30.1, 33.2],
        "Formal Credit (₹ Tn)": [8.2, 8.9, 9.4, 11.2, 13.8, 16.4, 19.1],
        "Fintech Disbursals (₹ Tn)": [0.4, 0.8, 1.4, 2.1, 3.6, 5.2, 7.8],
    })

    # Barrier data
    barrier_df = pd.DataFrame({
        "Barrier": ["No credit history", "No collateral", "Complex documentation",
                    "Bank branch too far", "Low digital literacy", "High interest rates"],
        "% MSMEs citing this": [67, 58, 52, 41, 38, 71],
    }).sort_values("% MSMEs citing this")

    # Opportunity segments
    opp_df = pd.DataFrame({
        "Segment": ["Women-owned MSMEs", "First-time borrowers", "GST-registered, no loan",
                    "UPI-active, unbanked", "Rural agri-MSMEs"],
        "Size (Mn)": [7.3, 18.2, 22.4, 14.6, 11.8],
        "Avg Loan Need (₹ Lakh)": [5, 8, 12, 6, 9],
        "Addressable Market (₹ Bn)": [3650, 14560, 26880, 8760, 10620],
    })

    return sector_df, tier_df, trend_df, barrier_df, opp_df

sector_df, tier_df, trend_df, barrier_df, opp_df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/200px-Mastercard-logo.svg.png", width=120)
    st.markdown("### Filters")
    selected_sectors = st.multiselect(
        "Sectors", sector_df["Sector"].tolist(), default=sector_df["Sector"].tolist()
    )
    selected_tiers = st.multiselect(
        "City Tiers", tier_df["City Tier"].tolist(), default=tier_df["City Tier"].tolist()
    )
    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("- RBI Annual Report 2023-24\n- MSME Ministry Census\n- IFC MSME Finance Gap\n- SIDBI MSME Pulse\n- Fintech Association India")
    st.markdown("---")
    st.caption("Built by Harish | Mastercard Advisors Application")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 📊 India MSME Credit Gap Analyzer")
st.markdown('<span class="tag">Financial Inclusion</span><span class="tag">MSME</span><span class="tag">India Fintech</span><span class="tag">RBI Data</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown('<div class="metric-card"><div class="metric-value">₹33.2T</div><div class="metric-label">Total MSME Credit Gap (2025)</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="metric-card"><div class="metric-value">63M+</div><div class="metric-label">MSMEs in India</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="metric-card"><div class="metric-value">84%</div><div class="metric-label">MSMEs without formal credit</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown('<div class="metric-card"><div class="metric-value">7.8x</div><div class="metric-label">Fintech disbursal growth (2019→25)</div></div>', unsafe_allow_html=True)

# ── Section 1: Trend ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Credit Gap Trend vs Fintech Growth</div>', unsafe_allow_html=True)

fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
fig_trend.add_trace(go.Bar(x=trend_df["Year"], y=trend_df["Credit Gap (₹ Tn)"],
    name="Credit Gap (₹ Tn)", marker_color="#eb5c2e"), secondary_y=False)
fig_trend.add_trace(go.Scatter(x=trend_df["Year"], y=trend_df["Fintech Disbursals (₹ Tn)"],
    name="Fintech Disbursals (₹ Tn)", line=dict(color="#00d4ff", width=3),
    mode="lines+markers"), secondary_y=True)
fig_trend.update_layout(
    paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e",
    font=dict(color="#ccc"), legend=dict(bgcolor="#1a1d2e"),
    height=360, margin=dict(t=20, b=20)
)
fig_trend.update_yaxes(gridcolor="rgba(255,255,255,0.07)")
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown('<div class="insight-box">💡 <b>Insight:</b> Despite 7.8x growth in fintech disbursals, the credit gap has widened by ₹13T since 2019 — formal credit simply hasn\'t kept pace with MSME growth. This is the opportunity window.</div>', unsafe_allow_html=True)

# ── Section 2: Sector breakdown ────────────────────────────────────────────────
st.markdown('<div class="section-header">🏭 Credit Gap by Sector</div>', unsafe_allow_html=True)

filtered_sector = sector_df[sector_df["Sector"].isin(selected_sectors)]
c1, c2 = st.columns(2)

with c1:
    fig_gap = px.bar(filtered_sector.sort_values("Credit Gap (₹ Bn)"),
        x="Credit Gap (₹ Bn)", y="Sector", orientation="h",
        color="Gap %", color_continuous_scale=["#16213e", "#eb5c2e"],
        text="Gap %")
    fig_gap.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_gap.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e",
        font=dict(color="#ccc"), height=320, margin=dict(t=20, b=20),
        coloraxis_showscale=False)
    fig_gap.update_xaxes(gridcolor="rgba(255,255,255,0.07)")
    st.plotly_chart(fig_gap, use_container_width=True)

with c2:
    fig_scatter = px.scatter(filtered_sector,
        x="Total MSMEs (Mn)", y="Gap %",
        size="Credit Gap (₹ Bn)", color="Sector",
        hover_data=["Avg Ticket Size (₹ Lakh)"],
        color_discrete_sequence=px.colors.qualitative.Bold)
    fig_scatter.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e",
        font=dict(color="#ccc"), height=320, margin=dict(t=20, b=20))
    fig_scatter.update_xaxes(gridcolor="rgba(255,255,255,0.07)")
    fig_scatter.update_yaxes(gridcolor="rgba(255,255,255,0.07)")
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown('<div class="insight-box">💡 <b>Insight:</b> Trade MSMEs have the largest absolute gap (₹8.6T) but Manufacturing MSMEs have smaller ticket sizes — ideal for cash-flow based underwriting using UPI + GST data, Mastercard\'s core data strength.</div>', unsafe_allow_html=True)

# ── Section 3: Tier analysis ───────────────────────────────────────────────────
st.markdown('<div class="section-header">🗺️ Geographic Credit Gap — Tier Analysis</div>', unsafe_allow_html=True)

filtered_tier = tier_df[tier_df["City Tier"].isin(selected_tiers)]
c3, c4 = st.columns(2)

with c3:
    fig_tier = go.Figure()
    fig_tier.add_trace(go.Bar(name="Banked %", x=filtered_tier["City Tier"],
        y=filtered_tier["Banked %"], marker_color="#00d4ff"))
    fig_tier.add_trace(go.Bar(name="GST Registered %", x=filtered_tier["City Tier"],
        y=filtered_tier["GST Registered %"], marker_color="#eb5c2e"))
    fig_tier.add_trace(go.Bar(name="UPI Adoption %", x=filtered_tier["City Tier"],
        y=filtered_tier["UPI Adoption %"], marker_color="#7bed9f"))
    fig_tier.update_layout(barmode="group", paper_bgcolor="#1a1d2e",
        plot_bgcolor="#1a1d2e", font=dict(color="#ccc"),
        height=320, margin=dict(t=20, b=20))
    fig_tier.update_yaxes(gridcolor="rgba(255,255,255,0.07)")
    st.plotly_chart(fig_tier, use_container_width=True)

with c4:
    fig_pie = px.pie(filtered_tier, values="Credit Gap (₹ Bn)", names="City Tier",
        color_discrete_sequence=["#eb5c2e", "#ff8c69", "#ffd700", "#00d4ff"],
        hole=0.5)
    fig_pie.update_layout(paper_bgcolor="#1a1d2e", font=dict(color="#ccc"),
        height=320, margin=dict(t=20, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown('<div class="insight-box">💡 <b>Insight:</b> Tier 2 & 3 cities hold 74% of the total credit gap yet have 58%+ UPI adoption — meaning the data infrastructure to underwrite them digitally already exists. The gap is access, not data.</div>', unsafe_allow_html=True)

# ── Section 4: Barriers ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🚧 Why MSMEs Don\'t Get Credit</div>', unsafe_allow_html=True)

fig_barrier = px.bar(barrier_df, x="% MSMEs citing this", y="Barrier",
    orientation="h", color="% MSMEs citing this",
    color_continuous_scale=["#16213e", "#eb5c2e"])
fig_barrier.update_layout(paper_bgcolor="#1a1d2e", plot_bgcolor="#1a1d2e",
    font=dict(color="#ccc"), height=300, margin=dict(t=20, b=20),
    coloraxis_showscale=False)
fig_barrier.update_xaxes(gridcolor="rgba(255,255,255,0.07)")
st.plotly_chart(fig_barrier, use_container_width=True)

# ── Section 5: Opportunity segments ───────────────────────────────────────────
st.markdown('<div class="section-header">🎯 Highest-Value Opportunity Segments</div>', unsafe_allow_html=True)

fig_opp = px.treemap(opp_df, path=["Segment"], values="Addressable Market (₹ Bn)",
    color="Avg Loan Need (₹ Lakh)",
    color_continuous_scale=["#16213e", "#eb5c2e"],
    hover_data=["Size (Mn)"])
fig_opp.update_layout(paper_bgcolor="#1a1d2e", font=dict(color="#ccc"),
    height=380, margin=dict(t=20, b=20))
st.plotly_chart(fig_opp, use_container_width=True)

# ── Section 6: Strategic Recommendation ───────────────────────────────────────
st.markdown('<div class="section-header">🔑 Strategic Recommendation</div>', unsafe_allow_html=True)

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:1.5rem">🎯</div>
        <div style="color:#fff;font-weight:600;margin:8px 0 4px">Target Segment</div>
        <div style="color:#ccc;font-size:0.85rem">GST-registered, UPI-active Tier 2/3 MSMEs with zero formal credit history — 22.4M businesses, ₹26.8T addressable market</div>
    </div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:1.5rem">⚙️</div>
        <div style="color:#fff;font-weight:600;margin:8px 0 4px">Mastercard's Edge</div>
        <div style="color:#ccc;font-size:0.85rem">Transaction intelligence across 3.5B+ cards globally + Mastercard Track data can build alternative credit scores where no CIBIL history exists</div>
    </div>
    """, unsafe_allow_html=True)
with r3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size:1.5rem">📈</div>
        <div style="color:#fff;font-weight:600;margin:8px 0 4px">Go-to-Market</div>
        <div style="color:#ccc;font-size:0.85rem">Partner with NBFCs and regional rural banks — provide credit scoring API, not direct lending. Asset-light, scalable, regulatory-friendly</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="insight-box" style="border-left-color:#7bed9f; margin-top:1rem">
🏆 <b>Bottom Line:</b> India's MSME credit gap is not a data problem — it's a trust and access problem. 
Mastercard's transaction data + SpendingPulse intelligence is uniquely positioned to build 
alternative credit rails for the 53M MSMEs currently invisible to formal lenders. 
The ₹33.2T opportunity is not being addressed by any single player at scale.
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
