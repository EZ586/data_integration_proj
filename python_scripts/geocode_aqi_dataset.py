import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Initialize geocoder with longer timeout
geolocator = Nominatim(user_agent="geo_lookup", timeout=5)

# Cache to store already fetched lat/lon to reduce API calls
geo_cache = {}

def get_lat_lon(cbsa):
    """Fetch latitude and longitude for a given CBSA using geopy with caching."""
    if not cbsa:
        return None, None

    # Check cache first
    if cbsa in geo_cache:
        return geo_cache[cbsa]

    try:
        location = geolocator.geocode(cbsa)
        if location:
            geo_cache[cbsa] = (location.latitude, location.longitude)
            return location.latitude, location.longitude
    except (GeocoderTimedOut, GeocoderUnavailable):
        print(f"Could not retrieve coordinates for {cbsa}")

    # If geocode fails, store None to avoid redundant requests
    geo_cache[cbsa] = (None, None)
    return None, None

def process_air_quality_data(input_csv, output_csv):
    """Processes air quality data and adds latitude/longitude based on CBSA."""
    df = pd.read_csv(input_csv)

    # Extract city from CBSA
    df["CITY"] = df["CBSA"].apply(lambda x: x.split(",")[0].upper())

    unhealthy_categories = {"Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous"}

    total_days_per_city = df.groupby("CITY")["Date"].count()
    unhealthy_days_per_city = df[df["Category"].isin(unhealthy_categories)].groupby("CITY")["Date"].count()

    percent_unhealthy = (unhealthy_days_per_city / total_days_per_city * 100).fillna(0)

    # Get latitude and longitude for each CBSA
    latitudes = []
    longitudes = []
    cbsas = df.groupby("CITY")["CBSA"].first()  # Get the first CBSA per city

    for city in percent_unhealthy.index:
        cbsa = cbsas.get(city, None)  # Get the CBSA for this city
        lat, lon = get_lat_lon(cbsa) if cbsa else (None, None)
        print(f"Processed {city}: {lat}, {lon}")
        latitudes.append(lat)
        longitudes.append(lon)
        time.sleep(1.1)  # Enforce 1.1-second delay to comply with API rate limits

    final_df = pd.DataFrame({
        "CITY": percent_unhealthy.index,
        "CBSA": cbsas,
        "Percent_Unhealthy_Days": percent_unhealthy.values,
        "Latitude": latitudes,
        "Longitude": longitudes
    })

    final_df.to_csv(output_csv, index=False)
    print(f"Processed data saved to {output_csv}")

# Example usage
process_air_quality_data("../raw_datasets/daily_aqi_by_cbsa_2019.csv", "geocoded_aqi_dataset.csv")
