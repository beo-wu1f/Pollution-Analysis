import requests
import os
import json
import datetime
import pandas as pd
import sqlite3
import glob

pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

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

# City information
city_name = "Mumbai"
country_code = "IN"

# Access the API key from the environment variable
api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

# Geocoding API endpoint
geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={api_key}"

# number of days you want data of
num_days = 10

 # Create a directory with today's date in YYYY-MM-DD format
today = datetime.datetime.today().strftime("%Y-%m-%d")
data_dir = os.path.join("data", today)
os.makedirs(data_dir, exist_ok=True)
print(f"Directory created: {data_dir}")

def create_and_save_data(city_name, country_code, api_key, num_days):
    """Fetches air pollution data, creates CSV, and stores data in SQLite."""
    # Send geocoding request
    geo_response = requests.get(geo_url)

    # Check response status
    if geo_response.status_code == 200:
        geo_data = geo_response.json()
        latitude = geo_data[0]["lat"]
        longitude = geo_data[0]["lon"]
        print("Latitudes and Longitudes received")
        
        try:
            # Create an empty DataFrame to store all daily data
            combined_df = pd.DataFrame(columns=pollutants + ['date'])

            for i in range(num_days):
                # Calculate timestamps for a single day
                past_date = datetime.datetime.today().date() - datetime.timedelta(days=i)
                start_timestamp = int(datetime.datetime(past_date.year, past_date.month, past_date.day, 0, 0).timestamp())
                end_timestamp = int(datetime.datetime(past_date.year, past_date.month, past_date.day, 23, 59).timestamp())

                historical_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={latitude}&lon={longitude}&start={start_timestamp}&end={end_timestamp}&appid={api_key}"
                historical_response = requests.get(historical_url)

                if historical_response.status_code == 200:
                    historical_data = historical_response.json()

                    # Calculate daily averages for this day's data
                    daily_averages = calculate_daily_averages(historical_data) 
                    print("Daily averages calculated")
                  
                    # Generate CSV for this day and save in the directory
                    for date, air_quality in daily_averages.items():
                        df = pd.DataFrame(air_quality, index=[0])
                        csv_path = os.path.join(data_dir, f"{date}.csv")
                        df.to_csv(csv_path, index=False)
                        print(" CSV Created")
                    
                else:
                    print(f"Error fetching historical data for {past_date.strftime('%Y-%m-%d')}: {historical_response.status_code}")

            # Combine all CSVs into a single DataFrame
            all_files = glob.glob(os.path.join(data_dir, '*.csv'))
            combined_df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)
            combined_df.to_csv(os.path.join(data_dir, 'combined_air_quality.csv'), index=False)

            # SQLite database handling
            db_path = os.path.join(data_dir, 'air_quality.db')
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS air_quality (
            date text,
            co real,
            no real,
            no2 real,
            o3 real,
            so2 real,
            pm2_5 real,
            pm10 real,
            nh3 real
            )''')

            for date, air_quality in daily_averages.items():
                c.execute("INSERT INTO air_quality VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (date, air_quality['co'], air_quality['no'], air_quality['no2'], air_quality['o3'], 
                            air_quality['so2'], air_quality['pm2_5'], air_quality['pm10'], air_quality['nh3']))

            conn.commit()
            conn.close()
            print("code executed, database created")

        except Exception as e:
            print(f"Error: {e}")

    else:
        print(f"Error: Geocoding API returned status code {geo_response.status_code}")        

create_and_save_data(city_name, country_code, api_key, num_days)
