import requests
import os

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

    # Print the coordinates
    lat = data['lat']
    lon = data['lon']
    print lat
    print lon
else:
    # Handle HTTP errors
    print(f"Error: {response.status_code}")
