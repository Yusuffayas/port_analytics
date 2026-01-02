import pandas as pd

def load_and_prepare_vessels(yearly_file):
    yearly_sheets = pd.read_excel(yearly_file, sheet_name=None)

    if "VESSELS" not in yearly_sheets:
        raise ValueError("VESSELS sheet not found")

    vessels_df = yearly_sheets["VESSELS"].copy()

    # Handle merged week cells
    vessels_df["Month"] = vessels_df["Month"].ffill()

    # Clean column names
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

    # Keep only week rows
    vessels_df = vessels_df[
        vessels_df["Month"]
        .astype(str)
        .str.lower()
        .str.contains("week")
    ]

    # Remove weekly subtotal rows
    vessels_df = vessels_df[vessels_df["Vessel Name"].notna()]

    # Extract week number
    vessels_df["Week"] = (
        vessels_df["Month"]
        .astype(str)
        .str.extract(r"(\d+)")
        .astype(int)
    )

    # Numeric safety
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

    return vessels_df

