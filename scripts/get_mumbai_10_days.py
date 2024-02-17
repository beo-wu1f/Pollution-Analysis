import requests
import os
import json
import datetime
import matplotlib.pyplot as plt

pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

def fetch_air_pollution_data(latitude, longitude, api_key):
    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    air_response = requests.get(air_url)
    if air_response.status_code == 200:
        return air_response.json()
    else:
        raise Exception(f"Air pollution API returned status code {air_response.status_code}")

def calculate_daily_averages(data):
    daily_averages = {}
    for hour_data in data['list']:
        # Extract the date
        date_str = datetime.datetime.fromtimestamp(hour_data['dt']).strftime('%Y-%m-%d')

        if date_str not in daily_averages:
            daily_averages[date_str] = {pollutant: 0 for pollutant in pollutants}

        for pollutant, value in hour_data['components'].items():
            daily_averages[date_str][pollutant] += value

    # Calculate averages for each component for each day
    for date, component_data in daily_averages.items():
        for pollutant, total in component_data.items():
            daily_averages[date][pollutant] = total / 24  # Average across 24 hours

    return daily_averages

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
    geo_data = geo_response.json()
    latitude = geo_data[0]["lat"]
    longitude = geo_data[0]["lon"]

    try:
        all_data = [] 
        for i in range(10):
            past_date = datetime.datetime.today().date() - datetime.timedelta(days=i)
            start_timestamp = int(datetime.datetime(past_date.year, past_date.month, past_date.day, 0, 0).timestamp())
            end_timestamp = int(datetime.datetime(past_date.year, past_date.month, past_date.day, 23, 59).timestamp())

            historical_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={latitude}&lon={longitude}&start={start_timestamp}&end={end_timestamp}&appid={api_key}"

            historical_response = requests.get(historical_url)

            if historical_response.status_code == 200:
                historical_data = historical_response.json()
                all_data.append(historical_data) 
            else:
                print(f"Error fetching historical data for {past_date.strftime('%Y-%m-%d')}: {historical_response.status_code}")

        # Calculate and print daily averages
            all_dates = []
            all_averages = []
        for day_data in all_data:
            daily_averages = calculate_daily_averages(day_data)
            date = list(daily_averages.keys())[0]  
            all_dates.append(date)
            all_averages.append(list(daily_averages.values())[0]) 

            # Print daily averages (you can remove this if you only want the plot)
            print(f"\nDaily Averages for {date}:")
            print(daily_averages[date])
        # Generate the filename with a timestamp
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"mumbai_air_pollution_{timestamp_str}.png"
        # Plot each pollutant
        for pollutant, values in all_averages[0].items():  
            plt.plot(all_dates, [data[pollutant] for data in all_averages], label=pollutant)
        plt.savefig(filename) 

    except Exception as e:
        print(f"Error: {e}")

else:
    print(f"Error: Geocoding API returned status code {geo_response.status_code}")


# Prepare data for plotting and calculate daily averages (combined functionality)


plt.xlabel("Date")
plt.ylabel("Average Pollutant Concentration")
plt.title("Average Air Pollution Over 10 Days in Mumbai")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()  
plt.show()
