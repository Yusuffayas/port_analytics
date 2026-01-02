import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🚢 Weekly Vessel Performance Analytics")

# =============================
# FILE UPLOAD
# =============================
yearly_file = st.file_uploader(
    "Upload YEARLY Vessel Excel",
    type=["xlsx"],
    key="yearly"
)

if not yearly_file:
    st.info("Please upload the YEARLY Excel file to proceed.")
    st.stop()

# =============================
# LOAD REQUIRED SHEET
# =============================
yearly_sheets = pd.read_excel(yearly_file, sheet_name=None)

if "VESSELS" not in yearly_sheets:
    st.error("VESSELS sheet not found in uploaded Excel.")
    st.stop()

vessels_df = yearly_sheets["VESSELS"].copy()

# =============================
# HANDLE MERGED WEEK CELLS
# =============================
vessels_df["Month"] = vessels_df["Month"].ffill()

# =============================
# CLEAN COLUMN NAMES
# =============================
vessels_df.columns = (
    vessels_df.columns
    .astype(str)
    .str.replace("\n", " ")
    .str.replace("  ", " ")
    .str.strip()
)

rename_map = {
    "Total Moves": "Total_Moves",
    "Total Units": "Total_Units",
    "Total TEUs": "Total_TEUs",
    "Weighted GCR": "Weighted_GCR"
}
vessels_df.rename(columns=rename_map, inplace=True)

# =============================
# KEEP ONLY WEEK ROWS
# =============================
vessels_df = vessels_df[
    vessels_df["Month"]
    .astype(str)
    .str.lower()
    .str.contains("week")
]

# =============================
# 🚨 REMOVE WEEKLY SUBTOTAL ROWS
# =============================
vessels_df = vessels_df[vessels_df["Vessel Name"].notna()]

# =============================
# EXTRACT WEEK NUMBER
# =============================
vessels_df["Week"] = (
    vessels_df["Month"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(int)
)

# =============================
# NUMERIC SAFETY
# =============================
numeric_cols = [
    "Total_Moves",
    "Total_Units",
    "Total_TEUs",
    "Hours",
    "Weighted_GCR",
    "OOG",
    "Bin Box",
    "Hatch Cover",
    "CI",
    "Forecast"
]

for col in numeric_cols:
    if col in vessels_df.columns:
        vessels_df[col] = pd.to_numeric(vessels_df[col], errors="coerce")

# =============================
# WEEKLY KPI (MATCHES EXCEL TOTAL ROW)
# =============================
weekly_kpi = (
    vessels_df
    .groupby("Week", as_index=False)
    .agg(
        Total_Moves=("Total_Moves", "sum"),
        Total_Units=("Total_Units", "sum"),
        Total_TEUs=("Total_TEUs", "sum"),
        Total_Hours=("Hours", "sum"),
        Avg_Weighted_GCR=("Weighted_GCR", "mean")
    )
    .sort_values("Week")
)

# =============================
# DISPLAY KPI TABLE
# =============================
st.subheader("📊 Weekly Vessel KPI Table (Excel-Verified)")
st.dataframe(weekly_kpi, use_container_width=True)

# =============================
# AUDIT / VERIFICATION SECTION
# =============================
st.subheader("🔍 Audit Check – Vessels Included Per Week")

selected_week = st.selectbox(
    "Select Week to Verify",
    weekly_kpi["Week"].tolist()
)

audit_df = vessels_df[vessels_df["Week"] == selected_week]

st.write(f"Vessels contributing to **Week {selected_week}**:")
st.dataframe(
    audit_df[
        [
            "Month",
            "Vessel Name",
            "Total_Moves",
            "Total_Units",
            "Total_TEUs",
            "Weighted_GCR"
        ]
    ],
    use_container_width=True
)

st.info(
    "✔ Only individual vessels are included.\n"
    "❌ Weekly subtotal rows are excluded to avoid double counting."
)

# =============================
# TREND CHART
# =============================
st.subheader("📈 Weekly Throughput Trend (TEUs)")

fig = px.line(
    weekly_kpi,
    x="Week",
    y="Total_TEUs",
    markers=True,
    title="Weekly TEU Throughput (No Double Count)"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 🧠 COMPLETE WEEKLY VESSEL PERFORMANCE INSIGHTS
# =====================================================
st.subheader("🧠 Weekly Vessel Performance – Complete Insights")

weekly_insights = (
    vessels_df
    .groupby("Week")
    .agg(
        Vessel_Count=("Vessel Name", "count"),

        # Volume
        Total_TEUs=("Total_TEUs", "sum"),
        Total_Units=("Total_Units", "sum"),
        Total_Moves=("Total_Moves", "sum"),

        # Time
        Total_Hours=("Hours", "sum"),

        # Productivity
        Avg_GCR=("Weighted_GCR", "mean"),

        # Operational complexity
        Total_OOG=("OOG", "sum"),
        Total_BinBox=("Bin Box", "sum"),
        Hatch_Cover_Count=("Hatch Cover", "sum"),
        CI_Count=("CI", "sum"),

        # Forecast (safe aggregation)
        Forecast_Units=("Forecast", "sum")
    )
    .reset_index()
)

# =============================
# DERIVED METRICS (SAFE)
# =============================
weekly_insights["TEUs_per_Vessel"] = (
    weekly_insights["Total_TEUs"] / weekly_insights["Vessel_Count"]
)

weekly_insights["Hours_per_Vessel"] = (
    weekly_insights["Total_Hours"] / weekly_insights["Vessel_Count"]
)

weekly_insights["TEUs_per_Hour"] = (
    weekly_insights["Total_TEUs"] / weekly_insights["Total_Hours"]
)

weekly_insights["Moves_per_Hour"] = (
    weekly_insights["Total_Moves"] / weekly_insights["Total_Hours"]
)

weekly_insights["Forecast_Deviation_%"] = (
    (weekly_insights["Total_Units"] - weekly_insights["Forecast_Units"])
    / weekly_insights["Forecast_Units"]
) * 100

# =============================
# DISPLAY FINAL INSIGHTS TABLE
# =============================
display_cols = [
    "Week",
    "Vessel_Count",
    "Total_TEUs",
    "Total_Units",
    "Total_Moves",
    "Total_Hours",
    "Avg_GCR",
    "TEUs_per_Hour",
    "Moves_per_Hour",
    "TEUs_per_Vessel",
    "Hours_per_Vessel",
    "Total_OOG",
    "Total_BinBox",
    "CI_Count",
    "Forecast_Deviation_%"
]

st.dataframe(
    weekly_insights[display_cols].round(2),
    use_container_width=True
)

st.subheader("📌 Weekly Performance Snapshot")

best_week = weekly_insights.loc[weekly_insights["Total_TEUs"].idxmax()]
worst_week = weekly_insights.loc[weekly_insights["Total_TEUs"].idxmin()]

avg_teus = weekly_insights["Total_TEUs"].mean()
avg_teus_per_hour = weekly_insights["TEUs_per_Hour"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🚀 Best Week (TEUs)",
    f"Week {int(best_week['Week'])}",
    f"{int(best_week['Total_TEUs'])} TEUs"
)

c2.metric(
    "⚠️ Worst Week (TEUs)",
    f"Week {int(worst_week['Week'])}",
    f"{int(worst_week['Total_TEUs'])} TEUs"
)

c3.metric(
    "📦 Avg Weekly TEUs",
    f"{avg_teus:,.0f}"
)

c4.metric(
    "⚙️ Avg TEUs / Hour",
    f"{avg_teus_per_hour:.2f}"
)

st.subheader("📈 Throughput vs Working Hours")

fig_hours = px.line(
    weekly_insights,
    x="Week",
    y=["Total_TEUs", "Total_Hours"],
    markers=True,
    title="Weekly Throughput vs Working Hours"
)

fig_hours.update_layout(
    yaxis_title="Value",
    legend_title="Metric"
)

st.plotly_chart(fig_hours, use_container_width=True)

st.subheader("🎯 Efficiency vs Load Analysis")

fig_scatter = px.scatter(
    weekly_insights,
    x="Total_TEUs",
    y="TEUs_per_Hour",
    size="Vessel_Count",
    color="Total_OOG",
    hover_name="Week",
    title="Efficiency vs Load (Bubble Size = Vessel Count)",
    labels={
        "Total_TEUs": "Total TEUs (Weekly Load)",
        "TEUs_per_Hour": "Efficiency (TEUs / Hour)",
        "Total_OOG": "OOG Complexity"
    }
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("⚠️ Operational Risk Weeks")

avg_hours = weekly_insights["Total_Hours"].mean()
avg_efficiency = weekly_insights["TEUs_per_Hour"].mean()

def classify_week(row):
    if row["TEUs_per_Hour"] < avg_efficiency and row["Total_Hours"] > avg_hours:
        return "🔴 High Risk – Low Efficiency, High Hours"
    elif row["Total_OOG"] > weekly_insights["Total_OOG"].mean():
        return "🟡 Warning – High OOG Complexity"
    else:
        return "🟢 Normal"

weekly_insights["Status"] = weekly_insights.apply(classify_week, axis=1)

risk_table = weekly_insights[
    ["Week", "Status", "Total_TEUs", "TEUs_per_Hour", "Total_Hours", "Total_OOG"]
]

st.dataframe(risk_table, use_container_width=True)



