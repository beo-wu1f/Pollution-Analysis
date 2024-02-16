import requests
import os
import json
from datetime import datetime

pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

def fetch_air_pollution_data(latitude, longitude, api_key):
  air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
  air_response = requests.get(air_url)
  if air_response.status_code == 200:
    return air_response.json()
  else:
    raise Exception(f"Air pollution API returned status code {air_response.status_code}")

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
    # Fetch air pollution data for last 30 days
    past_data = []
    for i in range(30):
      # Calculate date for past day
      past_date = datetime.date.today() - datetime.timedelta(days=i)
      past_date_str = past_date.strftime("%Y-%m-%d")

      # Construct historical air pollution API url
      historical_url = f"http://api.openweathermap.org/data/2.5/air_pollution/historical?lat={latitude}&lon={longitude}&dt={past_date_str}&appid={api_key}"

      # Send historical data request
      historical_response = requests.get(historical_url)

      if historical_response.status_code == 200:
        historical_data = historical_response.json()
        past_data.append(historical_data)
      else:
        print(f"Error fetching historical data for {past_date_str}: {historical_response.status_code}")

    # Print pollution data for each day
    for day_data in past_data:
      print(f"\nAir pollution data for {day_data['dt_iso']}:")
      for pollutant in pollutants:
        concentration = day_data["list"][0]["components"][pollutant]
        print(f"{pollutant}: {concentration} μg/m³")

  except Exception as e:
    print(f"Error: {e}")

else:
  print(f"Error: Geocoding API returned status code {geo_response.status_code}")
