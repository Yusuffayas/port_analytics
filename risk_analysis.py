def classify_risk(weekly_insights):
    avg_hours = weekly_insights["Total_Hours"].mean()
    avg_efficiency = weekly_insights["TEUs_per_Hour"].mean()

    def classify(row):
        if row["TEUs_per_Hour"] < avg_efficiency and row["Total_Hours"] > avg_hours:
            return "🔴 High Risk – Low Efficiency, High Hours"
        elif row["Total_OOG"] > weekly_insights["Total_OOG"].mean():
            return "🟡 Warning – High OOG Complexity"
        else:
            return "🟢 Normal"

    weekly_insights["Status"] = weekly_insights.apply(classify, axis=1)

    return weekly_insights
