import numpy as np
import scipy.stats as stats
import geopandas as gpd
import sys
import os


def calculate_confidence_interval(data, confidence=0.95):
  """
    Calculate the confidence interval for a 2D dataset.
    Parameters:
        data (np.array): 2D array where each row is a data point [x, y].
        confidence (float): Confidence level for the interval.
    Returns:
        (tuple): Lower and upper bounds for each dimension [(x_lower, x_upper), (y_lower, y_upper)].
    """
  # Calculate means and standard deviations
  means = np.mean(data, axis=0)
  std_devs = np.std(data, axis=0, ddof=1)  # Using sample std deviation (N-1)

  # Number of samples
  n = data.shape[0]

  # Calculate the margin of error
  margin_of_error = stats.t.ppf((1 + confidence) / 2., n - 1) * (std_devs / np.sqrt(n))

  # Confidence intervals for each dimension
  confidence_intervals = [(means[i] - margin_of_error[i], means[i] + margin_of_error[i]) for i in range(len(means))]

  return confidence_intervals


def points_within_ci(data, confidence_intervals):
  """
    Find points that lie within the given confidence intervals.
    Parameters:
        data (np.array): 2D array where each row is a data point [x, y].
        confidence_intervals (list): List of tuples representing the confidence intervals for each dimension.
    Returns:
        (np.array): Points that lie within the confidence intervals.
    """
  x_interval, y_interval = confidence_intervals

  # Logical condition to find points within the intervals
  within_x = (data[:, 0] >= x_interval[0]) & (data[:, 0] <= x_interval[1])
  within_y = (data[:, 1] >= y_interval[0]) & (data[:, 1] <= y_interval[1])

  # Combine conditions for both dimensions
  within_both = within_x & within_y

  return data[within_both]


# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

dataset = gpd.read_file("./tests/kano.csv")

# Extract Longitude and Latitude columns as float arrays
longitude = dataset['Longitude'].astype(float).values
latitude = dataset['Latitude'].astype(float).values

# Merge the data into a 2D array
data = np.array(list(zip(longitude, latitude)))

# Calculate the confidence intervals
confidence_intervals = calculate_confidence_interval(data, confidence=0.95)
print("Confidence Intervals:", confidence_intervals)

# Find points within the confidence intervals
points_in_ci = points_within_ci(data, confidence_intervals)
print("Points within Confidence Intervals:")
print(points_in_ci)
