import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point
import matplotlib as mpl

df = pd.read_csv("../processed_datasets/merged_aqi_revenue_geocode_dataset.csv")
df["Average_AQI"] = pd.to_numeric(df["Average_AQI"], errors="coerce")
df["Total_Rev_Prog_Desc"] = pd.to_numeric(df["Total_Rev_Prog_Desc"], errors="coerce")
min_aqi, max_aqi = df["Average_AQI"].min(), df["Average_AQI"].max()
df["Normalized_AQI"] = (df["Average_AQI"] - min_aqi) / (max_aqi - min_aqi)
min_rev, max_rev = df["Total_Rev_Prog_Desc"].min(), df["Total_Rev_Prog_Desc"].max()
df["Normalized_Revenue"] = (df["Total_Rev_Prog_Desc"] - min_rev) / (max_rev - min_rev)

def aqi_to_pm25(aqi):
    if aqi <= 50:
        return (aqi/50)*12.0
    elif aqi <= 100:
        return ((aqi-50)/50)*(35.4-12.1)+12.1
    elif aqi <= 150:
        return ((aqi-100)/50)*(55.4-35.5)+35.5
    elif aqi <= 200:
        return ((aqi-150)/50)*(150.4-55.5)+55.5
    else:
        return 150.4

gdf = gpd.GeoDataFrame(df, geometry=df.apply(lambda r: Point(r["Longitude"], r["Latitude"]), axis=1), crs="EPSG:4326").to_crs(epsg=3857)
fixed_bounds = gdf.total_bounds
initial_increase = 0.0
df["New_AQI"] = df["Average_AQI"] * (1 + initial_increase)
df["New_PM25"] = df["New_AQI"].apply(aqi_to_pm25)
df["Risk_Factor"] = 1 + (df["New_PM25"] / 10) * 0.06
df["New_Composite_Need"] = df["Risk_Factor"] - df["Normalized_Revenue"]
initial_values = df["New_Composite_Need"].values

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(fixed_bounds[0], fixed_bounds[2])
ax.set_ylim(fixed_bounds[1], fixed_bounds[3])
ax.set_axis_off()
try:
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs="EPSG:3857", reset_extent=False)
except Exception as e:
    print("Error adding basemap:", e)
scatter = ax.scatter(gdf.geometry.x, gdf.geometry.y, c=initial_values, cmap="coolwarm", s=100, edgecolor="k")
norm = mpl.colors.Normalize(vmin=0.95, vmax=1.05)
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
sm._A = []
cbar = fig.colorbar(sm, ax=ax, orientation="vertical")
cbar.set_label("Composite Need")
ax.set_title(f"Composite Need Heatmap (AQI increase: {initial_increase*100:.0f}%)")

ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
slider = Slider(ax_slider, "AQI Increase (%)", 0.0, 0.5, valinit=initial_increase, valstep=0.05)

def update(val):
    aqi_increase = slider.val
    df["New_AQI"] = df["Average_AQI"] * (1 + aqi_increase)
    df["New_PM25"] = df["New_AQI"].apply(aqi_to_pm25)
    df["Risk_Factor"] = 1 + (df["New_PM25"] / 10) * 0.06
    df["New_Composite_Need"] = df["Risk_Factor"] - df["Normalized_Revenue"]
    new_values = df["New_Composite_Need"].values
    scatter.set_array(new_values)
    ax.set_title(f"Composite Need Heatmap (AQI increase: {aqi_increase*100:.0f}%)")
    ax.set_xlim(fixed_bounds[0], fixed_bounds[2])
    ax.set_ylim(fixed_bounds[1], fixed_bounds[3])
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
