import streamlit as st
import plotly.express as px

def weekly_trend_chart(weekly_kpi):
    fig = px.line(
        weekly_kpi,
        x="Week",
        y="Total_TEUs",
        markers=True,
        title="Weekly TEU Throughput (No Double Count)"
    )
    st.plotly_chart(fig, use_container_width=True)


def throughput_vs_hours(weekly_insights):
    fig = px.line(
        weekly_insights,
        x="Week",
        y=["Total_TEUs", "Total_Hours"],
        markers=True,
        title="Weekly Throughput vs Working Hours"
    )
    st.plotly_chart(fig, use_container_width=True)


def efficiency_scatter(weekly_insights):
    fig = px.scatter(
        weekly_insights,
        x="Total_TEUs",
        y="TEUs_per_Hour",
        size="Vessel_Count",
        color="Total_OOG",
        hover_name="Week",
        title="Efficiency vs Load"
    )
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st

def render_audit_check(vessels_df, weekly_kpi):
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

