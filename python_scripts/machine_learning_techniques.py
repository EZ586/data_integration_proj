

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

def categorize_aqi(dataset_path="avg_aqi_revenue_data.csv"):
    

    # Load the CSV file (assumes only rows with both AQI and revenue are present)
    df = pd.read_csv("avg_aqi_revenue_data.csv")

    # Convert columns to numeric if needed
    df["Total_Rev_Prog_Desc"] = pd.to_numeric(df["Total_Rev_Prog_Desc"], errors="coerce")
    df["Average_AQI"] = pd.to_numeric(df["Average_AQI"], errors="coerce")

    # Normalize the features using MinMaxScaler so they are on a comparable scale.
    scaler = MinMaxScaler()
    df[['Normalized_AQI', 'Normalized_Revenue']] = scaler.fit_transform(df[['Average_AQI', 'Total_Rev_Prog_Desc']])

    # Compute a composite score: higher AQI and lower revenue yield a higher need score.
    df["Composite_Score"] = df["Normalized_AQI"] - df["Normalized_Revenue"]

    # --- Machine Learning Categorization using K-means clustering ---
    # We'll cluster the data into 3 groups (for example: high, moderate, low need)
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df[['Normalized_AQI', 'Normalized_Revenue']])

    # Identify which cluster corresponds to high need.
    # Here, we assume that a higher composite score implies a higher need.
    cluster_summary = df.groupby('Cluster')['Composite_Score'].mean()
    high_need_cluster = cluster_summary.idxmax()
    print("High-Need Cluster:", high_need_cluster)

    # Create a flag for high need areas
    df['High_Need'] = df['Cluster'] == high_need_cluster

    # Display high need cities
    print("\nHigh Need Areas:")
    print(df[df['High_Need']][["CITY", "Composite_Score", "Average_AQI", "Total_Rev_Prog_Desc"]])

    # --- Visualization: Correlation Heatmap ---
    # Create a correlation matrix for Average_AQI, Total_Rev_Prog_Desc, and Composite_Score
    corr = df[["Average_AQI", "Total_Rev_Prog_Desc", "Composite_Score"]].corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()

    # Visualize the clusters using a scatter plot
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x="Average_AQI", y="Total_Rev_Prog_Desc", hue="Cluster", palette="viridis", s=100)
    plt.title("Clusters based on Average_AQI and Total_Rev_Prog_Desc")
    plt.xlabel("Average AQI")
    plt.ylabel("Total Revenue")
    plt.show()

categorize_aqi()


