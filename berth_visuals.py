import streamlit as st
import plotly.express as px

def berth_occupancy_bar(df):
    fig = px.bar(
        df,
        x="Week",
        y="Berth_Occupancy_%",
        text=df["Berth_Occupancy_%"].round(1),
        title="🏗️ Weekly Berth Occupancy (%)",
        color="Berth_Occupancy_%",
        color_continuous_scale="RdYlGn_r"
    )

    fig.update_layout(
        yaxis_title="Occupancy %",
        xaxis_title="Week",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(fig, use_container_width=True)

def berth_usage_vs_capacity(df):
    fig = px.bar(
        df,
        x="Week",
        y=["Week_Port_Stay_Hrs_Plus_3", "Week_Total_Hrs"],
        title="⚓ Port Stay Hours vs Weekly Capacity",
        barmode="group",
        labels={"value": "Hours", "variable": "Metric"}
    )

    st.plotly_chart(fig, use_container_width=True)

def berth_efficiency_scatter(df):
    fig = px.scatter(
        df,
        x="Avg_GCR",
        y="Berth_Occupancy_%",
        size="Week_Port_Stay_Hrs",
        hover_name="Week",
        title="📈 Berth Efficiency Context (GCR vs Occupancy)",
        labels={
            "Avg_GCR": "Average GCR",
            "Berth_Occupancy_%": "Berth Occupancy %"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

def berth_occupancy_with_thresholds(df):
    import plotly.express as px
    import streamlit as st

    fig = px.line(
        df,
        x="Week",
        y="Berth_Occupancy_%",
        markers=True,
        title="📊 Berth Occupancy with Risk Thresholds"
    )

    fig.add_hline(y=70, line_dash="dot", annotation_text="Optimal (70%)")
    fig.add_hline(y=85, line_dash="dot", annotation_text="Congestion Risk (85%)")
    fig.add_hline(y=100, line_dash="dash", annotation_text="Over Capacity")

    fig.update_layout(yaxis_range=[0, 110])

    st.plotly_chart(fig, use_container_width=True)

def berth_buffer_loss(df):
    import plotly.express as px
    import streamlit as st

    fig = px.bar(
        df,
        x="Week",
        y="Buffer_Loss_%",
        title="⏱️ Capacity Lost Due to Buffer Time (+3 hrs)",
        text=df["Buffer_Loss_%"].round(2)
    )

    fig.update_layout(yaxis_title="Capacity Loss (%)")

    st.plotly_chart(fig, use_container_width=True)

def berth_productivity_quadrant(df):
    import plotly.express as px
    import streamlit as st

    fig = px.scatter(
        df,
        x="Avg_GCR",
        y="Berth_Occupancy_%",
        size="Week_Port_Stay_Hrs_Plus_3",
        hover_name="Week",
        title="📌 Productivity vs Congestion Quadrant"
    )

    fig.add_vline(
        x=df["Avg_GCR"].mean(),
        line_dash="dot",
        annotation_text="Avg GCR"
    )
    fig.add_hline(
        y=80,
        line_dash="dot",
        annotation_text="High Occupancy"
    )

    st.plotly_chart(fig, use_container_width=True)

def berth_weekly_delta(df):
    import plotly.express as px
    import streamlit as st

    df = df.copy()
    df["Occupancy_Δ"] = df["Berth_Occupancy_%"].diff()

    fig = px.bar(
        df,
        x="Week",
        y="Occupancy_Δ",
        title="📈 Week-to-Week Change in Berth Occupancy"
    )

    fig.update_layout(yaxis_title="Change in Occupancy (%)")

    st.plotly_chart(fig, use_container_width=True)

def berth_occupancy_heatmap(df):
    import plotly.express as px
    import streamlit as st

    heat_df = df.copy()
    heat_df["Week_Num"] = heat_df["Week"].str.extract(r"(\d+)").astype(int)

    fig = px.imshow(
        heat_df[["Berth_Occupancy_%"]].T,
        labels=dict(x="Week", color="Occupancy %"),
        x=heat_df["Week"],
        color_continuous_scale="Inferno",
        title="🔥 Weekly Berth Occupancy Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)

def berth_capacity_waterfall(df):
    import plotly.graph_objects as go
    import streamlit as st

    avg_stay = df["Week_Port_Stay_Hrs"].mean()
    avg_buffer = (
        df["Week_Port_Stay_Hrs_Plus_3"] - df["Week_Port_Stay_Hrs"]
    ).mean()

    fig = go.Figure(go.Waterfall(
        name="Capacity Flow",
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Total Capacity", "Port Stay", "Buffer Loss", "Remaining"],
        y=[168, -avg_stay, -avg_buffer, 0],
        connector={"line": {"color": "gray"}}
    ))

    fig.update_layout(
        title="⚓ Weekly Berth Capacity Utilization Flow",
        yaxis_title="Hours"
    )

    st.plotly_chart(fig, use_container_width=True)

def berth_occupancy_gauge(df):
    import plotly.graph_objects as go
    import streamlit as st

    avg_occ = df["Berth_Occupancy_%"].mean()

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_occ,
        title={"text": "Average Berth Occupancy (%)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 70], "color": "lightgreen"},
                {"range": [70, 85], "color": "orange"},
                {"range": [85, 100], "color": "red"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

