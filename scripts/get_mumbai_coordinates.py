import requests
import os
import json
import matplotlib.pyplot as plt

pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

def fetch_air_pollution_data(latitude, longitude, api_key):
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    air_response = requests.get(air_url)
    if air_response.status_code == 200:
        return air_response.json()
    else:
        raise Exception(f"Air pollution API returned status code {air_response.status_code}")

def plot_air_pollution_data(city_name, country_code, pollutants, concentrations):
    plt.figure(figsize=(10, 6))
    plt.bar(pollutants, concentrations)
    plt.xlabel("Pollutant")
    plt.ylabel("Concentration (μg/m³)")
    plt.title(f"Air Pollutant Concentrations in {city_name}, {country_code}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("air_pollution_visualization.png")
    plt.show()

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
        air_data = fetch_air_pollution_data(latitude, longitude, api_key)

        # Extract pollutant concentrations
        concentrations = [air_data["list"][0]["components"][pollutant] for pollutant in pollutants]

        # Display data
        print("Air pollutant concentrations in", city_name, country_code, ":\n")
        for i, pollutant in enumerate(pollutants):
            print(f"{pollutant}: {concentrations[i]} μg/m³")

        # Create and display visualization
        plot_air_pollution_data(city_name, country_code, pollutants, concentrations)

    except Exception as e:
        print(f"Error: {e}")

else:
    print(f"Error: Geocoding API returned status code {geo_response.status_code}")
