import pandas as pd

df_geo = pd.read_csv("../processed_datasets/geocoded_aqi_dataset.csv")

df_geo['CBSA'] = df_geo['CBSA'].str.upper()
df_rev = pd.read_csv("avg_aqi_revenue_data.csv")

merged_df = pd.merge(df_rev, df_geo, on="CBSA", how="inner")

final_df = merged_df[["CBSA", "City", "State", "Total_Rev_Prog_Desc", "Average_AQI", "Latitude", "Longitude"]]

# Save the final merged DataFrame to a CSV file
final_df.to_csv("../processed_datasets/merged_aqi_revenue_geocode_dataset.csv", index=False)

print("Merge complete. The merged data has been saved to 'merged_aqi_revenue_geocode_dataset.csv'.")
