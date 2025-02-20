import pandas as pd

df = pd.read_csv('datasets/CORE-2019-501C3-CHARITIES-PC-HRMN.csv')

sel_col = df[['F9_00_ORG_ADDR_CITY', 'SA_01_PCSTAT_ORG_AMT_SUPPORT_TOT']]

sel_col.to_csv('processed_datasets/new_file.csv', index=False)