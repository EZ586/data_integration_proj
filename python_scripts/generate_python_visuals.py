import pandas as pd
import matplotlib.pyplot as plt

def plot_scatter(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file, delimiter=',')  # Assuming tab-separated values
    print(df.columns.tolist())

    # Extract relevant columns
    x = df['Total_Rev_Prog_Desc']
    y = df['Percent_Unhealthy_Days']
    
    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.6, edgecolors='k')
    plt.xlabel('Total Revenue')
    plt.ylabel('Percent Unhealthy Days')
    plt.title('Scatter Plot of Revenue vs. Unhealthy Days')
    plt.xscale('log')  # Log scale for better visualization if values are large
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Show the plot
    plt.show()


plot_scatter('../processed_datasets/matched_city_info.csv')