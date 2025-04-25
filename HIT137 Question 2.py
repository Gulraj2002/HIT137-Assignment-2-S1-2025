#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import csv
from collections import defaultdict

# Configuration: Define the directory where the temperature data files are located.
DATA_DIRECTORY = 'temperature_data'

# Define a list of month names, which correspond to the column headers in the CSV files.
MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# Define a dictionary to represent the seasons and the months that belong to each season.
SEASONS = {
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August'],
    'Spring': ['September', 'October', 'November']
}

def load_temperature_data(data_directory):
    """
    This function reads temperature data from all CSV files found within the
    specified directory. Each CSV file is assumed to contain temperature readings
    for different months of a single year, along with a 'STATION_NAME' column.

    The function returns a dictionary where the keys are the names of the weather
    stations, and the values are lists of lists. Each inner list represents the
    monthly temperatures recorded for that station in a particular year.
    """
    all_data = defaultdict(list) # Use defaultdict to automatically create a list for new stations
    try:
        # Iterate through all files and directories within the specified data directory.
        for filename in os.listdir(data_directory):
            # Check if the current item is a file and if its name ends with '.csv'.
            if os.path.isfile(os.path.join(data_directory, filename)) and filename.endswith('.csv'):
                filepath = os.path.join(data_directory, filename)
                # Open each CSV file for reading. 'newline=''' ensures proper handling of line endings.
                with open(filepath, 'r', newline='') as csvfile:
                    # Create a CSV DictReader object to read the CSV file as dictionaries.
                    reader = csv.DictReader(csvfile)
                    # Check if the expected 'STATION_NAME' and the first month's header exist.
                    if MONTH_NAMES[0] not in reader.fieldnames or 'STATION_NAME' not in reader.fieldnames:
                        print(f"Warning: CSV file {filename} does not contain expected headers. Skipping.")
                        continue # Skip to the next file if headers are missing.
                    # Iterate over each row in the CSV file. Each row is a dictionary.
                    for row in reader:
                        station_name = row['STATION_NAME'] # Extract the station name from the row.
                        # Extract the monthly temperatures. Convert to float if a value exists, otherwise None.
                        monthly_temps = [float(row[month]) if row[month] else None for month in MONTH_NAMES]
                        all_data[station_name].append(monthly_temps) # Append the monthly data to the station's list.
    except FileNotFoundError:
        print(f"Error: Directory not found: {data_directory}")
    except Exception as e:
        print(f"An error occurred during data loading: {e}")
    return all_data # Return the dictionary containing temperature data for all stations.

# Load the temperature data by calling the load_temperature_data function.
station_temperatures = load_temperature_data(DATA_DIRECTORY)

# 1. Calculate the average temperature for each month across all years and stations.
monthly_average_temperatures = [[] for _ in MONTH_NAMES] # Initialize a list of empty lists for each month.
# Iterate through the temperature data for each station.
for station_data in station_temperatures.values():
    # Iterate through the yearly temperature data for the current station.
    for year_data in station_data:
        # Iterate through the temperatures for each month in the current year.
        for i, temp in enumerate(year_data):
            # Check if the temperature reading is not None before appending.
            if temp is not None:
                monthly_average_temperatures[i].append(temp) # Add the temperature to the corresponding month's list.

# Calculate the average temperature for each month by summing the temperatures and dividing by the count.
average_monthly_temps = {MONTH_NAMES[i]: sum(temps) / len(temps) if temps else 0 for i, temps in enumerate(monthly_average_temperatures)}

# Calculate the average temperature for each season across all years and stations.
seasonal_average_temperatures = {} # Initialize an empty dictionary to store seasonal averages.
# Iterate through the defined seasons and their corresponding months.
for season, months in SEASONS.items():
    seasonal_temps = [] # Initialize an empty list to store temperatures for the current season.
    # Get the indices of the months belonging to the current season.
    month_indices = [MONTH_NAMES.index(month) for month in months]
    # Iterate through the temperature data for each station.
    for station_data in station_temperatures.values():
        # Iterate through the yearly temperature data for the current station.
        for year_data in station_data:
            # Extract the temperatures for the months belonging to the current season.
            season_temps_year = [year_data[i] for i in month_indices if year_data[i] is not None]
            # Extend the seasonal_temps list with the valid temperatures for the current year.
            if season_temps_year:
                seasonal_temps.extend(season_temps_year)
    # Calculate the average temperature for the current season.
    seasonal_average_temperatures[season] = sum(seasonal_temps) / len(seasonal_temps) if seasonal_temps else 0

# Save the average monthly and seasonal temperatures to "average_temp.txt".
with open('average_temp.txt', 'w') as outfile:
    outfile.write("---------------------------------------\n")
    outfile.write("Average Monthly Temperatures (Celsius)\n")
    outfile.write("---------------------------------------\n")
    # Write the average temperature for each month to the output file.
    for month, avg_temp in average_monthly_temps.items():
        outfile.write(f"{month}: {avg_temp:.2f}\n")
    outfile.write("\n")
    outfile.write("----------------------------------------\n")
    outfile.write("Average Seasonal Temperatures (Celsius)\n")
    outfile.write("----------------------------------------\n")
    # Write the average temperature for each season to the output file.
    for season, avg_temp in seasonal_average_temperatures.items():
        outfile.write(f"{season}: {avg_temp:.2f}\n")

# 2. Find the station(s) with the largest temperature range.
station_temp_ranges = {} # Initialize a dictionary to store the temperature range for each station.
# Iterate through the temperature data for each station.
for station, data in station_temperatures.items():
    all_temps = [] # Initialize a list to store all valid temperatures for the current station.
    # Iterate through the yearly temperature data for the current station.
    for year_data in data:
        # Extend the all_temps list with valid (non-None) temperatures for the current year.
        all_temps.extend([temp for temp in year_data if temp is not None])
    # If there are valid temperatures for the station, calculate the temperature range.
    if all_temps:
        temp_range = max(all_temps) - min(all_temps) # Calculate the range (max - min).
        station_temp_ranges[station] = temp_range # Store the range in the dictionary.

largest_range = 0 # Initialize the variable to keep track of the largest temperature range found so far.
stations_with_largest_range = {} # Initialize a dictionary to store stations with the largest range.
# Iterate through the calculated temperature ranges for each station.
for station, temp_range in station_temp_ranges.items():
    # If the current station's temperature range is greater than the current largest range.
    if temp_range > largest_range:
        largest_range = temp_range # Update the largest range.
        stations_with_largest_range = {station: temp_range} # Reset the dictionary with the current station.
    # If the current station's temperature range is equal to the current largest range.
    elif temp_range == largest_range:
        stations_with_largest_range[station] = temp_range # Add the current station to the dictionary.

# Save the station(s) with the largest temperature range to "largest_temp_range_station.txt".
with open('largest_temp_range_station.txt', 'w') as outfile:
    outfile.write("---------------------------------------------------\n")
    outfile.write("Station(s) with the Largest Temperature Range (Celsius)\n")
    outfile.write("---------------------------------------------------\n")
    # Write each station with the largest temperature range and its range to the output file.
    for station, temp_range in stations_with_largest_range.items():
        outfile.write(f"{station}: {temp_range:.2f}\n")

# 3. Find the warmest and coolest station(s) based on average yearly temperature.
station_average_temps = {} # Initialize a dictionary to store the average yearly temperature for each station.
# Iterate through the temperature data for each station.
for station, data in station_temperatures.items():
    all_yearly_averages = [] # Initialize a list to store the average temperature for each year for the current station.
    # Iterate through the yearly temperature data for the current station.
    for year_data in data:
        # Filter out None values (missing temperature readings).
        valid_temps = [temp for temp in year_data if temp is not None]
        # If there are valid temperatures for the year, calculate the average.
        if valid_temps:
            all_yearly_averages.append(sum(valid_temps) / len(valid_temps))
    # If there are yearly averages for the station, calculate the overall average.
    if all_yearly_averages:
        station_average_temps[station] = sum(all_yearly_averages) / len(all_yearly_averages)

warmest_temp = float('-inf') # Initialize the warmest temperature found so far to negative infinity.
warmest_stations = {} # Initialize a dictionary to store the warmest station(s) and their average temperature.
coolest_temp = float('inf') # Initialize the coolest temperature found so far to positive infinity.
coolest_stations = {} # Initialize a dictionary to store the coolest station(s) and their average temperature.

# Iterate through the calculated average yearly temperatures for each station.
for station, avg_temp in station_average_temps.items():
    # Check if the current station's average temperature is greater than the current warmest temperature.
    if avg_temp > warmest_temp:
        warmest_temp = avg_temp # Update the warmest temperature.
        warmest_stations = {station: avg_temp} # Reset the warmest stations dictionary.
    # Check if the current station's average temperature is equal to the current warmest temperature.
    elif avg_temp == warmest_temp:
        warmest_stations[station] = avg_temp # Add the current station to the warmest stations dictionary.

    # Check if the current station's average temperature is less than the current coolest temperature.
    if avg_temp < coolest_temp:
        coolest_temp = avg_temp # Update the coolest temperature.
        coolest_stations = {station: avg_temp} # Reset the coolest stations dictionary.
    # Check if the current station's average temperature is equal to the current coolest temperature.
    elif avg_temp == coolest_temp:
        coolest_stations[station] = avg_temp # Add the current station to the coolest stations dictionary.

# Save the warmest and coolest station(s) to "warmest_and_coolest_station.txt".
with open('warmest_and_coolest_station.txt', 'w') as outfile:
    outfile.write("---------------------------------------------------\n")
    outfile.write("Warmest and Coolest Weather Stations (Average Celsius)\n")
    outfile.write("---------------------------------------------------\n")
    outfile.write("Warmest Station(s):\n")
    # Write each warmest station and its average temperature to the output file.
    for station, avg_temp in warmest_stations.items():
        outfile.write(f"- {station}: {avg_temp:.2f}\n")
    outfile.write("\nCoolest Station(s):\n")
    # Write each coolest station and its average temperature to the output file.
    for station, avg_temp in coolest_stations.items():
        outfile.write(f"- {station}: {avg_temp:.2f}\n")

# Print a message indicating that the analysis has been completed and the results have been saved.
print("Temperature analysis completed. Results saved to text files.")


# In[ ]:




