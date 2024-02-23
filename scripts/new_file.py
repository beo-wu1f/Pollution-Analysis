import requests
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, spearmanr

# *** Obtain your OpenWeatherMap API Key and replace the placeholder below ***
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

# City information
cities = [
    {'name': 'Mumbai', 'country_code': 'IN'},
    {'name': 'Delhi', 'country_code': 'IN'}
]

# Helper function for wind direction
def get_wind_direction(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = int((degrees + 22.5) / 45) % 8
    return directions[index]

# Function to fetch and process data (weather or pollution)
def fetch_and_process_data(city_name, country_code, api_key, data_type):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={api_key}"
    geo_response = requests.get(geo_url)

    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        latitude = geo_data[0]["lat"]
        longitude = geo_data[0]["lon"]

        if data_type == 'weather':
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        elif data_type == 'pollution':
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
        else:
            raise ValueError("Invalid data_type. Please use 'weather' or 'pollution'")

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API returned status code {response.status_code}")
    else:
        raise Exception(f"Geocoding API returned status code {geo_response.status_code}")

# Data collection, storage, and basic printing
datasets = {}

for city in cities:
    try:
        # Fetch & process weather data
        weather_data = fetch_and_process_data(city['name'], city['country_code'], api_key, 'weather')
        datasets[f"{city['name']} Weather"] = weather_data
        print(f"Weather data fetched for {city['name']}")

        # Fetch & process pollution data
        pollution_data = fetch_and_process_data(city['name'], city['country_code'], api_key, 'pollution')
        datasets[f"{city['name']} Pollution"] = pollution_data
        print(f"Pollution data fetched for {city['name']}")

    except Exception as e:
        print(f"Error for city {city['name']}: {e}")


# Basic Visualizations
for city_name, data_type in datasets.keys():
    data = datasets[city_name]

    if data_type.endswith('Weather'):
        print(f"\nGenerating plots for {city_name} Weather")
        plt.figure(figsize=(8, 4))
        plt.subplot(121)
        plt.bar(['Temperature'], [data['main']['temp']])
        plt.title("Temperature (Celsius)")        

        plt.subplot(122)
        plt.bar(['Humidity'], [data['main']['humidity']])
        plt.title("Humidity (%)")
        plt.tight_layout()
        plt.show()

    elif data_type.endswith('Pollution'):
        pollutants = data['list'][0]['components'].keys()
        concentrations = data['list'][0]['components'].values()

        plt.figure(figsize=(8, 4))
        plt.bar(pollutants, concentrations)
        plt.title(f"Air Pollutants in {city_name} (μg/m³)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
