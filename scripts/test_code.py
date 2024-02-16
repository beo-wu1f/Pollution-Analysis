import requests
import os
from datetime import datetime, timedelta
import json

pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
time_slots = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00']

def fetch_air_pollution_data(latitude, longitude, api_key, date_str, time_str):
    historical_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={latitude}&lon={longitude}&start={date_str}&end={date_str}&appid={api_key}"
    air_response = requests.get(historical_url)
    if air_response.status_code == 200:
        air_data = air_response.json()
        for slot in air_data['list']:
            if datetime.utcfromtimestamp(slot['dt']).strftime('%H:%M') == time_str:
                return slot
    return None

# Access the API key from the environment variable
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

# City information
city_name = "Mumbai"
country_code = "IN"

# Geocoding API endpoint
geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={api_key}"

# Send geocoding request
geo_response = requests.get(geo_url)

# Check response status
if geo_response.status_code == 200:
    # Parse JSON response
    geo_data = geo_response.json()

    # Extract latitude and longitude
    latitude = geo_data[0]["lat"]
    longitude = geo_data[0]["lon"]

    try:
        # Fetch air pollution data for last 10 days
        past_data = []
        for i in range(10):
            past_date = datetime.now() - timedelta(days=i)
            date_str = past_date.strftime("%Y-%m-%d")
            for time_slot in time_slots:
                data = fetch_air_pollution_data(latitude, longitude, api_key, date_str, time_slot)
                if data:
                    past_data.append(data)

        # Print pollution data for each time slot
        for day_data in past_data:
            print(f"\nAir pollution data for {datetime.utcfromtimestamp(day_data['dt']).strftime('%Y-%m-%d %H:%M')}:")
            for pollutant in pollutants:
                concentration = day_data["components"][pollutant]
                print(f"{pollutant}: {concentration} μg/m³")

    except Exception as e:
        print(f"Error: {e}")

else:
    print(f"Error: Geocoding API returned status code {geo_response.status_code}")
