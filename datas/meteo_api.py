#!/usr/bin/env python3
"""
Test Open-Meteo Weather & Air Quality APIs
Convert to separate DataFrames and analyze structure
"""

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

print("Testing Open-Meteo Weather & Air Quality APIs for NYC")
print("=" * 60)

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# NYC coordinates
NYC_LAT = 40.7128
NYC_LON = -74.0060

# ================================
# 1. WEATHER DATA
# ================================
print("\nFETCHING WEATHER DATA...")

weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": NYC_LAT,
    "longitude": NYC_LON,
    "hourly": [
        "temperature_2m",           # Temperature
        "apparent_temperature",     # Feels-like temperature  
        "precipitation",            # Rain/snow (mm)
        "rain",                    # Rain only (mm)
        "snowfall",                # Snow only (cm)
        "wind_speed_10m",          # Wind speed
        "wind_direction_10m",      # Wind direction
        "relative_humidity_2m",    # Humidity (%)
        "visibility",              # Visibility (m)
        "cloud_cover",             # Cloud cover (%)
        "weather_code",            # Weather condition code
        "pressure_msl",            # Sea level pressure
        "shortwave_radiation"      # Solar radiation
    ],
    "timezone": "America/New_York",
    "past_days": 2,  # Include 2 days of historical data for more context
}

try:
    weather_responses = openmeteo.weather_api(weather_url, params=weather_params)
    weather_response = weather_responses[0]
    
    print("Weather API Response:")
    print(f"   Coordinates: {weather_response.Latitude()}°N {weather_response.Longitude()}°E")
    print(f"   Elevation: {weather_response.Elevation()} m")
    print(f"   Timezone: {weather_response.UtcOffsetSeconds()}s offset from UTC")
    
    # Process weather data
    weather_hourly = weather_response.Hourly()
    weather_data = {
        "datetime": pd.date_range(
            start=pd.to_datetime(weather_hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(weather_hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=weather_hourly.Interval()),
            inclusive="left"
        ).tz_convert("America/New_York")
    }
    
    # Add each weather variable
    for i, param in enumerate(weather_params["hourly"]):
        weather_data[param] = weather_hourly.Variables(i).ValuesAsNumpy()
    
    # Create weather DataFrame
    weather_df = pd.DataFrame(weather_data)
    print(f"Weather DataFrame created: {weather_df.shape[0]} rows, {weather_df.shape[1]} columns")
    
except Exception as e:
    print(f"Weather API Error: {e}")
    weather_df = None

# ================================
# 2. AIR QUALITY DATA
# ================================
print("\nFETCHING AIR QUALITY DATA...")

air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
air_quality_params = {
    "latitude": NYC_LAT,
    "longitude": NYC_LON,
    "hourly": [
        "pm10",                    # Particulate Matter 10μm
        "pm2_5",                   # Particulate Matter 2.5μm
        "carbon_monoxide",         # CO
        "nitrogen_dioxide",        # NO2
        "sulphur_dioxide",         # SO2
        "ozone",                   # O3
        "ammonia",                 # NH3
        "aerosol_optical_depth",   # Atmospheric clarity
        "dust",                    # Dust particles
        "european_aqi",            # European Air Quality Index
        "european_aqi_pm2_5",      # AQI for PM2.5
        "european_aqi_pm10"        # AQI for PM10
    ],
    "timezone": "America/New_York",
    "past_days": 2,  # Include 2 days of historical data
}

try:
    air_quality_responses = openmeteo.weather_api(air_quality_url, params=air_quality_params)
    air_quality_response = air_quality_responses[0]
    
    print("Air Quality API Response:")
    print(f"   Coordinates: {air_quality_response.Latitude()}°N {air_quality_response.Longitude()}°E")
    print(f"   Elevation: {air_quality_response.Elevation()} m")
    
    # Process air quality data
    air_quality_hourly = air_quality_response.Hourly()
    air_quality_data = {
        "datetime": pd.date_range(
            start=pd.to_datetime(air_quality_hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(air_quality_hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=air_quality_hourly.Interval()),
            inclusive="left"
        ).tz_convert("America/New_York")
    }
    
    # Add each air quality variable
    for i, param in enumerate(air_quality_params["hourly"]):
        air_quality_data[param] = air_quality_hourly.Variables(i).ValuesAsNumpy()
    
    # Create air quality DataFrame
    air_quality_df = pd.DataFrame(air_quality_data)
    print(f"Air Quality DataFrame created: {air_quality_df.shape[0]} rows, {air_quality_df.shape[1]} columns")
    
except Exception as e:
    print(f"Air Quality API Error: {e}")
    air_quality_df = None

# ================================
# 3. DISPLAY RESULTS
# ================================
print("\n" + "=" * 60)
print("WEATHER DATA ANALYSIS")
print("=" * 60)

if weather_df is not None:
    print("\nWEATHER DataFrame Head:")
    print(weather_df.head())
    
    print("\nWEATHER DataFrame Info:")
    print(weather_df.info())
    
    print("\nWEATHER Data Summary:")
    print(f"   Time range: {weather_df['datetime'].min()} to {weather_df['datetime'].max()}")
    print(f"   Temperature range: {weather_df['temperature_2m'].min():.1f}°C to {weather_df['temperature_2m'].max():.1f}°C")
    print(f"   Total precipitation: {weather_df['precipitation'].sum():.1f} mm")
    print(f"   Max wind speed: {weather_df['wind_speed_10m'].max():.1f} km/h")
else:
    print("Weather data not available")

print("\n" + "=" * 60)
print("AIR QUALITY DATA ANALYSIS")
print("=" * 60)

if air_quality_df is not None:
    print("\nAIR QUALITY DataFrame Head:")
    print(air_quality_df.head())
    
    print("\nAIR QUALITY DataFrame Info:")
    print(air_quality_df.info())
    
    print("\nAIR QUALITY Data Summary:")
    print(f"   Time range: {air_quality_df['datetime'].min()} to {air_quality_df['datetime'].max()}")
    print(f"   PM2.5 range: {air_quality_df['pm2_5'].min():.1f} to {air_quality_df['pm2_5'].max():.1f} μg/m³")
    print(f"   PM10 range: {air_quality_df['pm10'].min():.1f} to {air_quality_df['pm10'].max():.1f} μg/m³")
    print(f"   European AQI range: {air_quality_df['european_aqi'].min():.0f} to {air_quality_df['european_aqi'].max():.0f}")
    
    # Check for data availability
    non_null_cols = air_quality_df.count()
    print("   Data availability:")
    for col in ['pm2_5', 'pm10', 'ozone', 'european_aqi']:
        if col in non_null_cols:
            pct = (non_null_cols[col] / len(air_quality_df)) * 100
            print(f"     {col}: {pct:.1f}% ({non_null_cols[col]}/{len(air_quality_df)} records)")
else:
    print("Air quality data not available")

# ================================
# 4. COMBINED ANALYSIS
# ================================
if weather_df is not None and air_quality_df is not None:
    print("\n" + "=" * 60)
    print("COMBINED DATA POTENTIAL")
    print("=" * 60)
    
    # Check time alignment
    weather_times = set(weather_df['datetime'])
    air_quality_times = set(air_quality_df['datetime'])
    common_times = weather_times.intersection(air_quality_times)
    
    print("Time alignment check:")
    print(f"   Weather data points: {len(weather_times)}")
    print(f"   Air quality data points: {len(air_quality_times)}")
    print(f"   Common timestamps: {len(common_times)}")
    print(f"   Overlap percentage: {(len(common_times) / max(len(weather_times), len(air_quality_times))) * 100:.1f}%")
    
    if len(common_times) > 0:
        print(f"\nReady for merge! Both datasets have {len(common_times)} matching timestamps")
        print("   Perfect for correlating weather conditions with air quality")
        print("   Can be easily joined with taxi trip data by datetime")
    
print("\n" + "=" * 60)
print("API TEST COMPLETE - Both weather and air quality data available!")
print("=" * 60)