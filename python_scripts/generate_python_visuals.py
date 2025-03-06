import pandas as pd
import matplotlib.pyplot as plt

def plot_scatter():
    # Load the CSV file
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

def plot_histogram():
    # Load the CSV file
    # Extract relevant columns
    x = df['Total_Rev_Prog_Desc']
    
    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.hist(x, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Total Revenue')
    plt.ylabel('Frequency')
    plt.title('Histogram of Total Revenue')
    plt.grid(axis='y', alpha=0.75)
    
    # Show the plot
    plt.show()



df = pd.read_csv('../processed_datasets/matched_city_info.csv', delimiter=',')

#plot_scatter()
plot_histogram()