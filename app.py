import streamlit as st

from berth_loader import load_berth_occupancy
from berth_metrics import compute_weekly_berth_metrics
from berth_visuals import (
    berth_occupancy_bar,
    berth_usage_vs_capacity,
    berth_efficiency_scatter,
    berth_occupancy_with_thresholds,
    berth_buffer_loss,
    berth_productivity_quadrant,
    berth_weekly_delta
)
from berth_visuals import berth_occupancy_heatmap
from berth_visuals import berth_capacity_waterfall
from berth_visuals import berth_occupancy_gauge


from data_loader import load_and_prepare_vessels
from weekly_kpi import (
    compute_weekly_kpi,
    compute_weekly_insights,
    render_weekly_snapshot
)
from risk_analysis import classify_risk
from visuals import (
    render_audit_check,
    weekly_trend_chart,
    throughput_vs_hours,
    efficiency_scatter
)

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(layout="wide")
st.title("🚢 Weekly Vessel Performance Analytics")

# =============================
# FILE UPLOAD
# =============================
yearly_file = st.file_uploader(
    "Upload YEARLY Vessel Excel",
    type=["xlsx"]
)

if not yearly_file:
    st.stop()

# =============================
# LOAD & PREPARE DATA
# =============================
vessels_df = load_and_prepare_vessels(yearly_file)

weekly_kpi = compute_weekly_kpi(vessels_df)

weekly_insights = compute_weekly_insights(vessels_df)
weekly_insights = classify_risk(weekly_insights)

# =============================
# 🔖 CATEGORY BAR (TABS)
# =============================
tab_kpi, tab_audit, tab_insights, tab_risk, tab_berth = st.tabs([
    "📊 Weekly KPIs",
    "🔍 Audit Check",
    "🧠 Performance Insights",
    "⚠️ Risk Analysis",
    "🏗️ Berth Analytics"
])

# =====================================================
# 📊 WEEKLY KPI TAB
# =====================================================
with tab_kpi:
    st.subheader("📊 Weekly Vessel KPI Table")
    st.dataframe(weekly_kpi, use_container_width=True)

    st.subheader("📈 Weekly Throughput Trend")
    weekly_trend_chart(weekly_kpi)

# =====================================================
# 🔍 AUDIT CHECK TAB
# =====================================================
with tab_audit:
    render_audit_check(vessels_df, weekly_kpi)

# =====================================================
# 🧠 PERFORMANCE INSIGHTS TAB
# =====================================================
with tab_insights:
    render_weekly_snapshot(weekly_insights)

    st.subheader("📋 Weekly Insights Table")
    st.dataframe(weekly_insights.round(2), use_container_width=True)

    st.subheader("📈 Throughput vs Working Hours")
    throughput_vs_hours(weekly_insights)

    st.subheader("🎯 Efficiency vs Load")
    efficiency_scatter(weekly_insights)

# =====================================================
# ⚠️ RISK ANALYSIS TAB
# =====================================================
with tab_risk:
    st.subheader("⚠️ Operational Risk Classification")

    st.dataframe(
        weekly_insights[
            [
                "Week",
                "Status",
                "Total_TEUs",
                "TEUs_per_Hour",
                "Total_Hours",
                "Total_OOG"
            ]
        ],
        use_container_width=True
    )

with tab_berth:
    st.subheader("🏗️ Berth Occupancy Analytics")

    berth_raw = load_berth_occupancy(yearly_file)
    berth_weekly = compute_weekly_berth_metrics(berth_raw)

    st.dataframe(
    berth_weekly.round(2).reset_index(drop=True),
    use_container_width=True
)


    berth_occupancy_bar(berth_weekly)
    berth_usage_vs_capacity(berth_weekly)
    berth_efficiency_scatter(berth_weekly)

    with st.expander("🧠 Berth Analytics – Key Insights"):
     peak = berth_weekly.loc[
        berth_weekly["Berth_Occupancy_%"].idxmax()
    ]

    st.markdown(f"""
    • Peak berth congestion occurred in **{peak['Week']}**
      with **{peak['Berth_Occupancy_%']:.1f}% occupancy**

    • Average weekly occupancy:
      **{berth_weekly['Berth_Occupancy_%'].mean():.1f}%**

    • Buffer time contributes to
      **{berth_weekly['Buffer_Loss_%'].mean():.2f}%**
      capacity loss per week
    """)

    st.subheader("📊 Occupancy with Risk Thresholds")
    berth_occupancy_with_thresholds(berth_weekly)

    st.subheader("⏱️ Buffer Time Capacity Loss")
    berth_buffer_loss(berth_weekly)

    st.subheader("📌 Productivity vs Congestion")
    berth_productivity_quadrant(berth_weekly)

    st.subheader("📈 Week-to-Week Occupancy Change")
    berth_weekly_delta(berth_weekly)

    berth_occupancy_heatmap(berth_weekly)
    berth_capacity_waterfall(berth_weekly)
    berth_occupancy_gauge(berth_weekly)


    

    

