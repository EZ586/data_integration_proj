import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.linear_model import LinearRegression
import numpy as np


def plot_scatter(
    ax, df, tested_feature, description, threshold=10**7, red_points_info=None, city_state_dict={}
):
    # Extract relevant columns
    x = df[tested_feature].values.reshape(-1, 1)
    y = df["Average_AQI"].values
    city_state_names = (df["F9_00_ORG_ADDR_CITY"] + ", " + df["F9_00_ORG_ADDR_STATE"]).values

    # Create scatter plot on the provided axes
    ax.scatter(x, y, alpha=0.6, edgecolors="k")
    ax.set_xlabel(tested_feature)
    ax.set_ylabel("Average_AQI Days")
    ax.set_title(f"Scatter Plot of {tested_feature} vs. Average_AQI")
    ax.set_xscale("log")  # Log scale for better visualization if values are large
    ax.grid(True, linestyle="--", alpha=0.6)

    # Fit linear regression model
    # Remove NaN and -inf values for fitting
    mask = ~np.isnan(x).flatten() & ~np.isnan(y) & (x.flatten() > 0)
    x_clean = x[mask].reshape(-1, 1)
    y_clean = y[mask]
    city_names_clean = city_state_names[mask]

    # Fit linear regression model
    model = LinearRegression()
    model.fit(np.log10(x_clean), y_clean)

    # Plot the trendline
    trendline_x = np.linspace(x_clean.min(), x_clean.max(), 100).reshape(-1, 1)
    trendline_y = model.predict(np.log10(trendline_x))
    ax.plot(trendline_x, trendline_y, color="red", linestyle="--", label="Trendline")
    ax.legend()

    # Add description as annotation
    ax.annotate(
        description, xy=(0.5, -0.1), xycoords="axes fraction", ha="center", fontsize=8
    )
    # Highlight points below the threshold and above the trendline
    predicted_y = model.predict(np.log10(x_clean))
    above_trendline = y_clean > predicted_y
    below_threshold = x_clean.flatten() < threshold
    highlight_mask = above_trendline & below_threshold

    # Calculate distances from the trendline for highlighted points
    distances = np.abs(y_clean[highlight_mask] - predicted_y[highlight_mask])

    # Sort highlighted points by distance from the trendline
    sorted_indices = np.argsort(-distances)  # Sort in descending order of distance
    sorted_cities = city_names_clean[highlight_mask][sorted_indices]
    sorted_x = x_clean[highlight_mask][sorted_indices]
    sorted_y = y_clean[highlight_mask][sorted_indices]
    sorted_distances = distances[sorted_indices]

    # Scatter the highlighted points in red
    ax.scatter(
        sorted_x,
        sorted_y,
        color="red",
        edgecolors="k",
        label="Highlighted Points",
    )

    # Collect information about the red points
    if red_points_info is not None:
        for city, x_val, y_val, distance in zip(
            sorted_cities, sorted_x.flatten(), sorted_y, sorted_distances
        ):
            red_points_info.append(
                f"City: {city}, X: {x_val}, Y: {y_val}, Distance from Trendline: {distance}"
            )
            # check if city is in city_state_dict
            if city not in city_state_dict:
                # set city to 0 if not in city_state_dict
                city_state_dict[city] = 0
            city_state_dict[city] += distance


# Load the CSV file
df = pd.read_csv("processed_datasets/City_Analysis.csv", delimiter=",")

# Load the descriptions from the CSV file
descriptions_df = pd.read_csv("datasets/CORE-HRMN_dd.csv")
descriptions_dict = descriptions_df.set_index("variable_name")[
    "variable_description"
].to_dict()

# Get all columns starting from the 3rd column
chosen_columns = [
    "F9_08_REV_PROG_DESC",
    "SA_02_PUB_SUPPORT_TOT",
    "F9_08_REV_OTH_FUNDR_EVNT_1",
    "F9_08_REV_OTH_FUNDR_DIRECT_EXP",
    "F9_08_REV_MISC_BIZCODE",
    "SA_02_TOT_SUPPORT_TOT",
    "SA_02_PUB_GIFT_GRANT_CONTR_TOT",
    "F9_09_EXP_FEE_SVC_ACC_TOT",
]

threshold_val = {
    "F9_08_REV_PROG_DESC": 10**7,
    "SA_02_PUB_SUPPORT_TOT": 10**7,
    "F9_08_REV_OTH_FUNDR_EVNT_1": 10**5,
    "F9_08_REV_OTH_FUNDR_DIRECT_EXP": 5.5 * 10**4,
    "F9_08_REV_MISC_BIZCODE": 10**7,
    "SA_02_TOT_SUPPORT_TOT": 10**7,
    "SA_02_PUB_GIFT_GRANT_CONTR_TOT": 10**7,
    "F9_09_EXP_FEE_SVC_ACC_TOT": 10**5,
}

city_state_dict = {}

# Calculate correlation with 'Average_AQI'
correlations = (
    df[chosen_columns].corrwith(df["Average_AQI"]).sort_values(ascending=False)
)

# Print the columns sorted by correlation
print(correlations)

# Create a list to store red points information
red_points_info = []

# Create a PDF file to save the plots
with PdfPages("chosen_scatter_plots.pdf") as pdf:
    # Plot the columns in groups of 2 per sheet
    num_plots = len(correlations)
    plots_per_figure = 2

    for start in range(0, num_plots, plots_per_figure):
        end = min(start + plots_per_figure, num_plots)
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        axes = axes.flatten()

        for i in range(start, end):
            tested_feature = correlations.index[i]
            description = descriptions_dict.get(
                tested_feature, "No description available"
            )
            red_points_info.append(f"{tested_feature}")
            plot_scatter(
                axes[i - start],
                df,
                tested_feature,
                description,
                threshold_val[tested_feature],
                red_points_info,
                city_state_dict
            )
            red_points_info.append("\n")

        # Adjust layout and save the figure to the PDF
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

# Save the red points information to a text file
with open("red_points_info.txt", "w") as f:
    f.write("\n".join(red_points_info))

print("All plots have been saved to chosen_scatter_plots.pdf")
print("Red points information has been saved to red_points_info.txt")
