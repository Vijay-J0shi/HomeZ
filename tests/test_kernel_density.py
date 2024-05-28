"""
CSV Format: [ No | id | Collar_id | date | time | Time(UTC) | Longitude | Latitude ]

For Day & Night instead of manipulating the KernelDensityEstimator algorithm,
seperate the data into day and night and get the value.

Day(AM) data: [area, plot]
Night(PM) data: [area, plot]
"""

import sys
import os
import geopandas as gpd
import pandas as pd

# Create a DataFrame
data = {
  'No': [1, 2, 3, 4, 5, 6],
  'id': [101, 102, 103, 104, 105, 106],
  'Collar_id': ['A1', 'A2', 'A1', 'A2', 'A1', 'A2'],
  'date': ['2024-05-01', '2024-05-01', '2024-05-02', '2024-05-02', '2024-05-01', '2024-05-02'],
  'time': ['12:00:00', '13:00:00', '14:00:00', '15:00:00', '11:00:00', '16:00:00'],
  'Time(UTC)': ['12:00', '13:00', '14:00', '15:00', '11:00', '16:00'],
  'Longitude': [-120.123, -120.124, -120.125, -120.126, -120.127, -120.128],
  'Latitude': [35.678, 35.679, 35.680, 35.681, 35.682, 35.683]}

df = pd.DataFrame(data)

# Convert to a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# Set the coordinate reference system (CRS)
gdf.set_crs(epsg=4326, inplace=True)

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
  from homez.home_range.utils import homez_distance_displacement, separate_day_night_coordinates
#  from homez.home_range.kernel_density import KernelDensityEstimator
except ImportError as e:
  print(f"Error: import module: {e}")
  sys.exit(1)

# Set the coordinate reference system (CRS)
gdf.set_crs(epsg=4326, inplace=True)
day_data, night_data = separate_day_night_coordinates(gdf, time_column="time")

print(homez_distance_displacement(day_data))

# # Day
# x_day = day_data.Longitude.astype(float)
# y_day = day_data.Latitude.astype(float)
#
# kde_day = KernelDensityEstimator(x_day, y_day)
# kde_day_res = kde_day.calculate(0.1)
#
# plot = kde_day_res
# # Open a file in write and binary mode
# with open("kde_day_test.tiff", 'wb') as file:
#   # Write the contents of the buffer to the file
#   file.write(plot.getvalue())
