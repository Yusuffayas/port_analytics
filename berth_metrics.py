import pandas as pd

WEEK_TOTAL_HOURS = 168  # fixed, confirmed

def compute_weekly_berth_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure numeric safety
    df["Avg_GCR"] = pd.to_numeric(df["Avg_GCR"], errors="coerce")
    df["Avg_BP"] = pd.to_numeric(df["Avg_BP"], errors="coerce")
    df["Week_Port_Stay_Hrs"] = pd.to_numeric(
        df["Week_Port_Stay_Hrs"], errors="coerce"
    )

    
   

    weekly = (
        df
        .groupby("Week", as_index=False)
        .agg(
            Avg_GCR=("Avg_GCR", "mean"),
            Avg_BP=("Avg_BP", "mean"),
            Week_Port_Stay_Hrs=("Week_Port_Stay_Hrs", "sum"),
            Week_Port_Stay_Hrs_Plus_3=("Week_Port_Stay_Hrs_Plus_3", "sum")
        )
    )

    weekly["Week_Total_Hrs"] = WEEK_TOTAL_HOURS

    weekly["Berth_Occupancy_%"] = (
        weekly["Week_Port_Stay_Hrs_Plus_3"] / WEEK_TOTAL_HOURS
    ) * 100

    weekly["Buffer_Loss_%"] = (
    (weekly["Week_Port_Stay_Hrs_Plus_3"] - weekly["Week_Port_Stay_Hrs"])
    / weekly["Week_Total_Hrs"]
) * 100


    # Proper week ordering (NO SERIAL NUMBER COLUMN)
    weekly["Week_Num"] = (
        weekly["Week"].astype(str).str.extract(r"(\d+)").astype(int)
    )
    weekly = weekly.sort_values("Week_Num").drop(columns="Week_Num")

    return weekly
