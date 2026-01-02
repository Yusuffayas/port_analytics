import pandas as pd

def load_berth_occupancy(file):
    sheets = pd.read_excel(file, sheet_name=None)

    if "Berth Occupancy" not in sheets:
        raise ValueError("Berth Occupancy sheet not found")

    # 🔹 Read with header in 2nd row (this was the ROOT problem)
    df = pd.read_excel(
        file,
        sheet_name="Berth Occupancy",
        header=1   # ⬅️ IMPORTANT
    )

    # 🔹 Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.replace("\n", " ")
        .str.replace("  ", " ")
        .str.strip()
    )

    # 🔹 Force Week column (first column)
    df = df.rename(columns={df.columns[0]: "Week"})
    df["Week"] = df["Week"].ffill()

    # 🔹 Keep only WEEKLY summary rows
    if "Week PORT STAY HRS" not in df.columns:
        raise KeyError(
            f"'Week PORT STAY HRS' not found. Columns are: {list(df.columns)}"
        )

    weekly_df = df[df["Week PORT STAY HRS"].notna()].copy()

    # 🔹 Rename exactly what we need
    weekly_df = weekly_df.rename(columns={
        "Average GCR": "Avg_GCR",
        "Average BP": "Avg_BP",
        "Week PORT STAY HRS": "Week_Port_Stay_Hrs",
        "Week PORT STAY HRS + 3": "Week_Port_Stay_Hrs_Plus_3"
    })

    # 🔹 Robust time conversion (NO split(':') nonsense)
    def to_hours(val):
        if pd.isna(val):
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        try:
            td = pd.to_timedelta(val)
            return td.total_seconds() / 3600
        except:
            return 0.0

    weekly_df["Week_Port_Stay_Hrs"] = (
        weekly_df["Week_Port_Stay_Hrs"].apply(to_hours)
    )
    weekly_df["Week_Port_Stay_Hrs_Plus_3"] = (
        weekly_df["Week_Port_Stay_Hrs_Plus_3"].apply(to_hours)
    )


    return weekly_df[
        ["Week", "Avg_GCR", "Avg_BP", "Week_Port_Stay_Hrs","Week_Port_Stay_Hrs_Plus_3"]
    ]
