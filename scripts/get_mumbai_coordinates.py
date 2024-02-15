import requests
import os
import json

# Access the API key from the environment variable
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

# City name, state code (not needed for India), and country code
city_name = "Mumbai"
country_code = "IN"

# API endpoint URL
url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={api_key}"

# Send API request
response = requests.get(url)

# Check response status
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    data_parse = json.loads(data)
    print(data_parse)
    print("\nLatitude:", data_parse["lat"])
    print("Longitude:", data_parse["lon"])
    if "local_names" in data:
        print("\nLocal name in Hindi:", data["local_names"]["hi"]

else:
    # Handle HTTP errors
    print(f"Error: {response.status_code}")
