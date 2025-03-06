import pandas as pd

# Load dataset
df = pd.read_csv('datasets/CORE-2019-501C3-CHARITIES-PC-HRMN.csv')
aqi_df = pd.read_csv('processed_datasets/processed_aqi_dataset.csv')


def city_revenue():
    # Select necessary columns
    sel_col = df[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'F9_08_REV_PROG_DESC']].copy()  # <== FIX: Use .copy()

    # Convert revenue column to numeric safely
    sel_col.loc[:, 'F9_08_REV_PROG_DESC'] = pd.to_numeric(sel_col['F9_08_REV_PROG_DESC'], errors='coerce')

    # Remove rows where revenue is NaN
    sel_col = sel_col.dropna(subset=['F9_08_REV_PROG_DESC'])

    # Group by city and state, summing revenue
    city_revenue = sel_col.groupby(['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'])['F9_08_REV_PROG_DESC'].sum().reset_index()

    # Rename columns for clarity
    city_revenue.columns = ['City', 'State', 'Total_Rev_Prog_Desc']

    # Save to CSV
    city_revenue.to_csv('processed_datasets/City_Revenue_Summary.csv', index=False)

    # Display the first few rows
    print(city_revenue.head())
    return city_revenue

def get_unique_cities():
    unique_values = df['F9_00_ORG_ADDR_CITY'].unique()
    with open('unique_cities.txt', 'w') as f:
        for value in unique_values:
            f.write(f"{value}\n")

def process_NCSS():
    # Select necessary columns
    sel_col = df[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'F9_08_REV_PROG_DESC']].copy()  # <== FIX: Use .copy()

    # Convert revenue column to numeric safely
    sel_col.loc[:, 'F9_08_REV_PROG_DESC'] = pd.to_numeric(sel_col['F9_08_REV_PROG_DESC'], errors='coerce')

    # Remove rows where revenue is NaN
    sel_col = sel_col.dropna(subset=['F9_08_REV_PROG_DESC'])

    # remove rows with no values for these columns
    df_filtered = sel_col.dropna(subset=['F9_00_ORG_NAME_L1', 'F9_08_REV_PROG_DESC'])
    df_filtered.to_csv('processed_datasets/Proccessed_CORE-2019-501C3-CHARITIES-PC-HRMN.csv', index=False)

def data_for_city_state():
    city_name = "ABILENE"
    state_name = "KS"

    filtered_data = df[(df['F9_00_ORG_ADDR_CITY'] == city_name) & (df['F9_00_ORG_ADDR_STATE'] == state_name)][['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'F9_08_REV_PROG_DESC']]
    filtered_data.to_csv('processed_datasets/city_state_data.csv', index=False)

def matched_cities():
    # Load first dataset (charities data)
    charities_df = df.copy()

    # Load second dataset (unhealthy days data)
    unhealthy_days_df = aqi_df

   # Extract city and state from charities dataset
    charities_cities_states = charities_df[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE']].drop_duplicates()

    # Extract city and state from unhealthy days dataset
    unhealthy_days_df['State'] = unhealthy_days_df['CBSA'].str.split(',').str[-1].str.strip()  # Create a separate State column
    unhealthy_cities_states = unhealthy_days_df[['CITY', 'State', 'Percent_Unhealthy_Days']].drop_duplicates()

    # Merge on both city and state (inner join keeps only matching city and state pairs)
    matching_cities_states = pd.merge(charities_cities_states, unhealthy_cities_states, 
                                    left_on=['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'], 
                                    right_on=['CITY', 'State'], how='inner')

    # Save to CSV
    matching_cities_states.to_csv('processed_datasets/matching_cities_states.csv', index=False)
    unhealthy_cities_states.to_csv('processed_datasets/unhealthy_cities_states.csv', index=False)

    # Display results
    print(matching_cities_states.head())
    return matching_cities_states[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'Percent_Unhealthy_Days']]

# THIS METHOD PRODUCES FINAL CSV FILE PROVIDED
def city_revenue_for_matched_cities():
    # Get the city revenue summary
    city_revenue_data = city_revenue()

    # Get the matched cities
    matched_cities_data = matched_cities()

    # Merge city revenue with matched cities data to filter for only matched cities
    matched_city_revenue = pd.merge(city_revenue_data, matched_cities_data, 
                                    left_on=['City', 'State'], 
                                    right_on=['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'], 
                                    how='inner')

    matched_city_revenue = matched_city_revenue[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'Total_Rev_Prog_Desc', 'Percent_Unhealthy_Days']]
    # Save the matched city revenue to a CSV file
    matched_city_revenue.to_csv('processed_datasets/matched_city_info.csv', index=False)

    # Display the first few rows of the matched city revenue data
    print(matched_city_revenue.head())
    
city_revenue_for_matched_cities()