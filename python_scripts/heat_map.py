import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the data from CSV file
df = pd.read_csv('processed_datasets/geocoded_aqi_dataset.csv')  # Replace with the actual file path

# Drop rows with missing Latitude or Longitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# Create a map centered around the US
us_map = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

# Prepare the data for HeatMap (Latitude, Longitude, Intensity)
heat_data = [[row['Latitude'], row['Longitude'], row['Percent_Unhealthy_Days']] for index, row in df.iterrows()]

# Add HeatMap to the map
HeatMap(heat_data).add_to(us_map)

# Save the map to an HTML file
us_map.save('us_heatmap_unhealthy_days.html')

# Display the map in a Jupyter notebook (optional)
us_map
