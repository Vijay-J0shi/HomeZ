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
data = gpd.read_file("./tests/kano.csv")

df = pd.DataFrame(data)

# Convert to a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# Set the coordinate reference system (CRS)
gdf.set_crs(epsg=4326, inplace=True)

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
  from homez.home_range.utils import separate_day_night_coordinates
  from homez.home_range.kernel_density import KernelDensityEstimator
except ImportError as e:
  print(f"Error: import module: {e}")
  sys.exit(1)

# Set the coordinate reference system (CRS)
gdf.set_crs(epsg=4326, inplace=True)
day_data, night_data = separate_day_night_coordinates(gdf, time_column="NST Time")

# Day
x_day = day_data.Longitude.astype(float)
y_day = day_data.Latitude.astype(float)

kde_day = KernelDensityEstimator(x_day, y_day)
kde_day_res = kde_day.calculate(0.5)

plot = kde_day_res
# Open a file in write and binary mode
with open("kde_day_test.tiff", 'wb') as file:
  # Write the contents of the buffer to the file
  file.write(plot.getvalue())
