# This code interacts with the SQLite database created in Code 4. It demonstrates SQL queries to fetch all data, 
# view data from the last 5 days, and find the day with the highest CO pollution.

import sqlite3
import pandas as pd

# Specify database path
db_path = 'data/2024-02-20/air_quality.db'

# Connect to the database
print("Connecting to the database...")
conn = sqlite3.connect(db_path)

# 1. View All Data 
print("Fetching all data from the database...")
query1 = """
SELECT * FROM air_quality;
"""
df = pd.read_sql_query(query1, conn)
print(df)

# 2. View Data (last 5 days)
print("Fetching data for the last 5 days...")
query2 = """
SELECT * FROM air_quality 
WHERE date >= date('now', '-5 days') 
ORDER BY date DESC;
"""
df = pd.read_sql_query(query2, conn)
print(df)

# 3. Day with the Highest CO Pollution
print("Fetching the day with the highest CO pollution...")
query3 = """
SELECT date, co
FROM air_quality
ORDER BY co DESC
LIMIT 1; 
"""
df = pd.read_sql_query(query3, conn)
print(df)

# Close the database connection
print("Closing database connection...")
conn.close()
