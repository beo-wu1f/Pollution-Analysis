import requests
import os
import json
import matplotlib.pyplot as plt

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
        # Parse JSON response
        air_data = air_response.json()

        # Extract pollutant concentrations
        concentrations = []
        pollutants = ["co", "NO", "NO2", "O3", "SO2", "PM2.5", "PM10", "NH3"]
        for pollutant in pollutants:
            concentrations.append(air_data["list"][0]["components"][pollutant])

        # Display data
        print("Air pollutant concentrations in", city_name, country_code, ":\n")
        for i, pollutant in enumerate(pollutants):
            print(f"{pollutant}: {concentrations[i]} μg/m³")

        # Create and display visualization
        plt.figure(figsize=(10, 6))
        plt.bar(pollutants, concentrations)
        plt.xlabel("Pollutant")
        plt.ylabel("Concentration (μg/m³)")
        plt.title("Air Pollutant Concentrations in Mumbai, India")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the visualization as a PNG image (optional)
        plt.savefig("air_pollution_visualization.png")

        # Display the visualization in a separate window
        plt.show()

    else:
        print(f"Error: Air pollution API returned {air_response.status_code}")

else:
    print(f"Error: Geocoding API returned {geo_response.status_code}")

