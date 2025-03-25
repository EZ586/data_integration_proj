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
    # print(matching_cities_states.head())
    return matching_cities_states[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'Percent_Unhealthy_Days']]
def matched_aqi():
    # Load first dataset (charities data)
    charities_df = df.copy()
    aqi_df = pd.read_csv('processed_datasets/average_aqi_data.csv')
    # Load second dataset (unhealthy days data)
    unhealthy_days_df = aqi_df

   # Extract city and state from charities dataset
    charities_cities_states = charities_df[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE']].drop_duplicates()

    # Extract city and state from unhealthy days dataset
    unhealthy_days_df['State'] = unhealthy_days_df['CBSA'].str.split(',').str[-1].str.strip()  # Create a separate State column
    unhealthy_cities_states = unhealthy_days_df[['CITY', 'State', 'Average_AQI']].drop_duplicates()

    # Merge on both city and state (inner join keeps only matching city and state pairs)
    matching_cities_states = pd.merge(charities_cities_states, unhealthy_cities_states, 
                                    left_on=['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'], 
                                    right_on=['CITY', 'State'], how='inner')

    # Display results
    # print(matching_cities_states.head())
    return matching_cities_states[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'Average_AQI']]

def analyze_headers():
    # Load dataset
    NCSS_df = pd.read_csv('datasets/CORE-2019-501C3-CHARITIES-PC-HRMN.csv')
    header_df = pd.read_csv('datasets/CORE-HRMN_dd.csv')
    # Only include headers with number type value in NCSS_df column value greater than 0
    numeric_columns = NCSS_df.select_dtypes(include=['number']).columns.tolist()
    # Filter columns where values are greater than 0
    nonzero_col = [col for col in numeric_columns if (NCSS_df[col] > 0).any()]
    # print((NCSS_df['F9_05_501C12_GRO_INCOME_MEMB'] > 0).any())
    filtered_rows = NCSS_df[NCSS_df['F9_05_501C12_GRO_INCOME_MEMB'] > 0][['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'F9_05_501C12_GRO_INCOME_MEMB']]
    # print(filtered_rows)

    test_df = NCSS_df.copy()[['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE', 'F9_05_501C12_GRO_INCOME_MEMB']]
    test_df = NCSS_df[NCSS_df['F9_05_501C12_GRO_INCOME_MEMB'] > 0]
    test_df.to_csv('processed_datasets/test_df.csv', index=False)

    headers_in_both_df = header_df[header_df['variable_name'].isin(nonzero_col)]
    
    # Write into text variable_name and corresponding variable_description
    with open('headers_in_both.txt', 'w') as f:
        for index, row in headers_in_both_df.iterrows():
            f.write(f"{row['variable_name']}: {row['variable_description']}\n")

    # get City State table with nonzero columns
    city_df = NCSS_df.groupby(['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'])[nonzero_col].sum().reset_index()
    city_nonzero_col = [col for col in nonzero_col if (city_df[col] > 0).any()]


    analyzed_columns = ['F9_05_501C12_GRO_INCOME_MEMB','F9_05_501C12_GRO_INCOME_OTH', 'F9_08_REV_OTH_FUNDR_EVNT_1']
    # analyzed_columns = city_nonzero_col
    city_analysis = NCSS_df.groupby(['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'])[city_nonzero_col].sum().reset_index()

    # add unhealthy days to city_analysis
    matched_cities_data = matched_aqi()
    city_analysis = pd.merge(city_analysis, matched_cities_data, 
                                        left_on=['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'], 
                                        right_on=['F9_00_ORG_ADDR_CITY', 'F9_00_ORG_ADDR_STATE'], 
                                        how='inner')
    # Save to CSV
    city_analysis.to_csv('processed_datasets/City_Analysis.csv', index=False)
    

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
    
analyze_headers()