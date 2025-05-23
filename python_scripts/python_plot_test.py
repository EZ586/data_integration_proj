import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

def plot_scatter(ax, df, tested_feature, description):
    # Extract relevant columns
    x = df[tested_feature]
    y = df['Average_AQI']
    
    # Create scatter plot on the provided axes
    ax.scatter(x, y, alpha=0.6, edgecolors='k')
    ax.set_xlabel(tested_feature)
    ax.set_ylabel('Average_AQI Days')
    ax.set_title(f'Scatter Plot of {tested_feature} vs. Average_AQI')
    ax.set_xscale('log')  # Log scale for better visualization if values are large
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Add description as annotation
    ax.annotate(description, xy=(0.5, -0.1), xycoords='axes fraction', ha='center', fontsize=8)

# Load the CSV file
df = pd.read_csv('processed_datasets/City_Analysis.csv', delimiter=',')

# Load the descriptions from the CSV file
descriptions_df = pd.read_csv('datasets/CORE-HRMN_dd.csv')
descriptions_dict = descriptions_df.set_index('variable_name')['variable_description'].to_dict()

# Get all columns starting from the 3rd column
columns_from_third = df.iloc[:, 2:].columns.to_list()

# Calculate correlation with 'Average_AQI'
correlations = df[columns_from_third].corrwith(df['Average_AQI']).sort_values(ascending=False)

# Print the columns sorted by correlation
print(correlations)

# Create a PDF file to save the plots
with PdfPages('scatter_plots.pdf') as pdf:
    # Plot the columns in groups of 2 per sheet
    num_plots = len(correlations)
    plots_per_figure = 2

    for start in range(0, num_plots, plots_per_figure):
        end = min(start + plots_per_figure, num_plots)
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        axes = axes.flatten()
        
        for i in range(start, end):
            tested_feature = correlations.index[i]
            description = descriptions_dict.get(tested_feature, 'No description available')
            plot_scatter(axes[i - start], df, tested_feature, description)
        
        # Adjust layout and save the figure to the PDF
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print("All plots have been saved to scatter_plots.pdf")