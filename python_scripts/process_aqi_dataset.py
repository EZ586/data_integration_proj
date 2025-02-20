import pandas as pd

def process_air_quality_data(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    df["CITY"] = df["CBSA"].apply(lambda x: x.split(",")[0].upper())

    unhealthy_categories = {"Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous"}

    total_days_per_city = df.groupby("CITY")["Date"].count()

    unhealthy_days_per_city = df[df["Category"].isin(unhealthy_categories)].groupby("CITY")["Date"].count()

    percent_unhealthy = (unhealthy_days_per_city / total_days_per_city * 100).fillna(0)

    final_df = pd.DataFrame({
        "CITY": percent_unhealthy.index,
        "CBSA": df.groupby("CITY")["CBSA"].first(),
        "Percent_Unhealthy_Days": percent_unhealthy.values
    })

    final_df.to_csv(output_csv, index=False)

    print(f"Processed data saved to {output_csv}")

process_air_quality_data("daily_aqi_by_cbsa_2019.csv", "processed_aqi_dataset.csv")
