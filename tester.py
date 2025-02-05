import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date

# Read the CSV file into a DataFrame
df = pd.read_csv('temperature.csv')

# Convert the 'date' column to datetime objects
df['date'] = pd.to_datetime(df['date'])

# Extract columns for x and y axes
x = date2num(df['date'])  # Convert datetime objects to numerical format
temperature = df['temperature']

# Create a scatter plot for temperature
plt.scatter(df['date'], temperature, label='Temperature Data')

# Calculate the regression line
slope, intercept = np.polyfit(x, temperature, 1)
regression_line = slope * x + intercept

# Convert numerical dates back to datetime objects for plotting
regression_dates = num2date(x)

# Plot the regression line
plt.plot(regression_dates, regression_line, color='red', label='Regression Line')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Data with Regression Line')
plt.legend()

# Show the plot
plt.show()
