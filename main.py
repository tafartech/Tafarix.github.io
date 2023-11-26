import requests
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import random

# Generate synthetic energy consumption data for one week
start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2023-12-31")
date_range = pd.date_range(start_date, end_date, freq="H")

energy_data = []
for timestamp in date_range:
    energy_usage = random.uniform(5, 30)  # Simulated energy consumption in kWh
    energy_data.append({"Timestamp": timestamp, "EnergyUsage_kWh": energy_usage})

# Create a Pandas DataFrame from the generated data
df = pd.DataFrame(energy_data)

# Save the data to a CSV file
df.to_csv("energy_consumption_data.csv", index=False)

print("Synthetic energy consumption data generated and saved to 'energy_consumption_data.csv'.")

# Load the energy consumption data from the CSV file
data = pd.read_csv("energy_consumption_data.csv")
data["Timestamp"] = pd.to_datetime(data["Timestamp"])
data.set_index("Timestamp", inplace=True)

# Perform time series decomposition
result = seasonal_decompose(data["EnergyUsage_kWh"], model="additive")
# Load the energy consumption data from the CSV file
data = pd.read_csv("energy_consumption_data.csv")

# Check the first few rows of the DataFrame
print(data.head())

# Check for missing values
missing_values = data.isnull().sum()
print("\nMissing Values:\n", missing_values)

# Summary statistics of the energy consumption column
summary_stats = data["EnergyUsage_kWh"].describe()
print("\nSummary Statistics:\n", summary_stats)
# Function to fetch climate change data
import os  # To access environment variables for the API key

# Function to fetch weather data using an API key provided via environment variable
def fetch_weather_data(api_key, city, start_date, end_date):
    base_url = "http://api.weatherapi.com/v1/history.json"
    # Assuming each day's data needs to be fetched individually
    date_range = pd.date_range(start_date, end_date, freq="D")
    weather_data = []
    
    for date in date_range:
        params = {
            "key": api_key,
            "q": city,
            "dt": date.strftime("%Y-%m-%d")
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Assuming we want to store daily average temperature
            avg_temp = data['forecast']['forecastday'][0]['day']['avgtemp_c']
            weather_data.append({"Date": date, "AvgTemp_C": avg_temp})
        else:
            print("Error fetching data for date:", date)

    # Convert to DataFrame
    weather_df = pd.DataFrame(weather_data)

    # Save the data as CSV
    weather_df.to_csv("weather_data.csv", index=False)
    print("Weather data saved to 'weather_data.csv'.")


city = "New York"  # Replace with your target city
start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2023-01-07")  # Replace with your desired end date
#fetch_weather_data(city, start_date, end_date)
plt.figure(figsize=(12, 6))
# Assuming we are plotting the whole dataset. You can slice the 'data' DataFrame if needed.
plt.plot(data.index, data['EnergyUsage_kWh'], color='green', label='Energy Consumption (kWh)')
# Since timestamps are on the x-axis, we need to just change their color, which is done by setting tick_params
plt.tick_params(axis='x', colors='blue')
plt.title('Energy Consumption Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Energy Consumption (kWh)')
plt.legend()  # This adds the legend to the plot
plt.show()
import networkx as nx

# Assuming 'data' is the Panda's DataFrame containing energy consumption data
# and we want to visualize the connections between hours and their energy usage

# Create a graph
G = nx.Graph()

# Add nodes and edges based on energy consumption data
for index, row in data.iterrows():
    node_name = row['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    energy = row['EnergyUsage_kWh']
    G.add_node(node_name, energy=energy)
    if G.number_of_nodes() > 1:
        # Connect each node to the previous one
        prev_node = data.loc[data.index[index - 1], 'Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        G.add_edge(prev_node, node_name, weight=1)

# Draw the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G)
edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
nx.draw(G, pos, node_color='b', edgelist=edges, edge_color='r', width=1, with_labels=True)
plt.title('Network Graph of Energy Consumption')
plt.show()