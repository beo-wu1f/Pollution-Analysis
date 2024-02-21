import os
import requests
import json

# City information
city_name = "Mumbai"
country_code = "IN"

# Access the API key from the environment variable
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

# Geocoding API endpoint
geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={api_key}"

def fetch_and_print_data(city_name, country_code, api_key):
    # Send geocoding request
    geo_response = requests.get(geo_url)

    # Check response status
    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        latitude = geo_data[0]["lat"]
        longitude = geo_data[0]["lon"]
        print("Latitudes and Longitudes received")

        try:
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
            weather_response = requests.get(weather_url)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                print(weather_data)

            else:
                print(f"Error fetching weather data for {latitude}, {longitude}: {weather_response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    else:
        print(f"Error: Geocoding API returned status code {geo_response.status_code}")

fetch_and_print_data(city_name, country_code, api_key)
