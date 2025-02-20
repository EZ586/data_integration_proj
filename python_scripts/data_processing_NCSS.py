import pandas as pd

# NCCS processing
df = pd.read_csv('datasets/CORE-2019-501C3-CHARITIES-PC-HRMN.csv')
sel_col = df[['EIN2','F9_00_ORG_NAME_L1','F9_00_ORG_ADDR_CITY','F9_00_ORG_ADDR_STATE','F9_08_REV_PROG_DESC']]

# Assuming 'df' is your DataFrame and you want the first row
row_index = 4  # Change this to the index of the row you want

# Get the row as a Series
row = df.iloc[row_index]

# Print each column name and its value
for column_name, value in row.items():
    if isinstance(value, (int, float)) and value > 1:
        print(f"{column_name}: {value}")

# get unique cities
# unique_values = df['F9_00_ORG_ADDR_CITY'].unique()
# with open('unique_cities.txt', 'w') as f:
#     for value in unique_values:
#         f.write(f"{value}\n")

# remove rows with no values for these columns
df_filtered = sel_col.dropna(subset=['F9_00_ORG_NAME_L1', 'F9_08_REV_PROG_DESC'])
df_filtered.to_csv('processed_datasets/Proccessed_CORE-2019-501C3-CHARITIES-PC-HRMN.csv', index=False)

