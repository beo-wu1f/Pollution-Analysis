import requests
import os  # Import the os module to access environment variables

# Access the API key from the environment variable
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

# City name, state code (not needed for India), and country code
city_name = "Mumbai"
country_code = "IN"

# API endpoint URL
url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={api_key}"

# Send API request
response = requests.get(url)

if response.status_code == 200:
    # Parse JSON response
    data = response.json()

    # Check if any results found
    if data["count"] > 0:
        # Get the first result (assuming Mumbai is the intended location)
        location = data["list"][0]

        # Print coordinates
        print("Latitude:", location["lat"])
        print("Longitude:", location["lon"])
    else:
        print("No results found for", city_name)
else:
    # Handle HTTP errors
    print(f"Error: {response.status_code}")
