import pandas as pd
def compute_weekly_kpi(vessels_df):
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
    return weekly_kpi


def compute_weekly_insights(vessels_df):
    weekly_insights = (
        vessels_df
        .groupby("Week")
        .agg(
            Vessel_Count=("Vessel Name", "count"),
            Total_TEUs=("Total_TEUs", "sum"),
            Total_Units=("Total_Units", "sum"),
            Total_Moves=("Total_Moves", "sum"),
            Total_Hours=("Hours", "sum"),
            Avg_GCR=("Weighted_GCR", "mean"),
            Total_OOG=("OOG", "sum"),
            Total_BinBox=("Bin Box", "sum"),
            Hatch_Cover_Count=("Hatch Cover", "sum"),
            CI_Count=("CI", "sum"),
            Forecast_Units=("Forecast", "sum")
        )
        .reset_index()
    )

    # Derived metrics
    weekly_insights["TEUs_per_Vessel"] = weekly_insights["Total_TEUs"] / weekly_insights["Vessel_Count"]
    weekly_insights["Hours_per_Vessel"] = weekly_insights["Total_Hours"] / weekly_insights["Vessel_Count"]
    weekly_insights["TEUs_per_Hour"] = weekly_insights["Total_TEUs"] / weekly_insights["Total_Hours"]
    weekly_insights["Moves_per_Hour"] = weekly_insights["Total_Moves"] / weekly_insights["Total_Hours"]
    weekly_insights["Forecast_Deviation_%"] = (
        (weekly_insights["Total_Units"] - weekly_insights["Forecast_Units"])
        / weekly_insights["Forecast_Units"]
    ) * 100

    return weekly_insights

import streamlit as st

def render_weekly_snapshot(weekly_insights):
    st.subheader("📌 Weekly Performance Snapshot")

    best_week = weekly_insights.loc[
        weekly_insights["Total_TEUs"].idxmax()
    ]

    worst_week = weekly_insights.loc[
        weekly_insights["Total_TEUs"].idxmin()
    ]

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

