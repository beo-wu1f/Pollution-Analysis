import requests
import os
import json

# API key (change placeholder with your actual key)
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

    # Air pollution API endpoint
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"

    # Send air pollution request
    air_response = requests.get(air_url)

    # Check response status
    if air_response.status_code == 200:
        # Print entire JSON response without parsing
        print(air_response.text)
    else:
        print(f"Error: Air pollution API returned {air_response.status_code}")
else:
    print(f"Error: Geocoding API returned {geo_response.status_code}")
