import pandas as pd

def process_air_quality_data(input_csv, output_csv):
    # Read the input CSV file
    df = pd.read_csv(input_csv)

    # Create a CITY column by extracting the city name from the CBSA field and converting it to uppercase
    df["CITY"] = df["CBSA"].apply(lambda x: x.split(",")[0].upper())

    # Calculate the average AQI per city
    average_aqi = df.groupby("CITY")["AQI"].mean()
    
    # Get the first CBSA entry per city (note the parentheses to call the method)
    first_cbsa = df.groupby("CITY")["CBSA"].first()

    # Build a new DataFrame with CITY, CBSA, and Average_AQI
    final_df = pd.DataFrame({
        "CITY": average_aqi.index,
        "CBSA": first_cbsa.values,  # Use .values to extract the actual data
        "Average_AQI": average_aqi.values
    })

    # Save the processed data to an output CSV file
    final_df.to_csv(output_csv, index=False)
    print(f"Processed data saved to {output_csv}")

def create_csv_with_average_aqi_and_nccs_data(aqi_data, revenue_data):
    # Load the average AQI data and standardize the CBSA column
    aqi_df = pd.read_csv(aqi_data)
    aqi_df["CBSA"] = aqi_df["CBSA"].str.upper().str.strip()

    # Load revenue data
    revenue_df = pd.read_csv(revenue_data)
    
    # Construct and standardize CBSA using City and State from revenue data
    revenue_df["CBSA"] = (revenue_df["City"].str.upper().str.strip() 
                          + ", " + 
                          revenue_df["State"].str.upper().str.strip())
    
    # Merge revenue data with average AQI data on CBSA (left merge ensures we keep all revenue entries)
    merged_df = pd.merge(revenue_df, aqi_df, on="CBSA", how="left")
    
    # Remove rows where either the Average_AQI or Total_Rev_Prog_Desc is missing
    merged_df = merged_df.dropna(subset=["Average_AQI", "Total_Rev_Prog_Desc"])

    # Save the merged dataset
    merged_df.to_csv("avg_aqi_revenue_data.csv", index=False)
    print("Merged data saved to avg_aqi_revenue_data.csv")


#process_air_quality_data("../raw_datasets/daily_aqi_by_cbsa_2019.csv", "average_aqi_data.csv")
create_csv_with_average_aqi_and_nccs_data("average_aqi_data.csv", "../processed_datasets/City_Revenue_Summary.csv")
