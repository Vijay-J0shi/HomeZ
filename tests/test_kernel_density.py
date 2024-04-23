"""
For Day & Night instead of manipulating the KernelDensityEstimator algorithm,
seperate the data into day and night and get the value.

Day(AM) data: [area, plot]
Night(PM) data: [area, plot]
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
  from homez.home_range.utils import utils, separate_day_night_coordinates
  from homez.home_range.kernel_density import KernelDensityEstimator
except ImportError as e:
  print(f"Error: import module: {e}")
  sys.exit(1)

dataset = "tests/sample.csv"

gdf = utils.read_shapefile(dataset)
gdf = gdf.dropna(subset=["x", "y"])

day_data, night_data = separate_day_night_coordinates(gdf, time_column="time")

# Day
x_day = day_data.x.astype(float)
y_day = day_data.y.astype(float)

kde_day = KernelDensityEstimator(x_day, y_day)
kde_day_res = kde_day.calculate(0.1)

print(kde_day_res[0])

plot = kde_day_res[1]
# Open a file in write and binary mode
with open("kde_day_test.tiff", 'wb') as file:
  # Write the contents of the buffer to the file
  file.write(plot.getvalue())

# Night
x_night = night_data.x.astype(float)
y_night = night_data.y.astype(float)

kde_day = KernelDensityEstimator(x_night, y_night)
kde_night_res = kde_day.calculate(0.5)

print(kde_night_res[0])

plot = kde_night_res[1]
# Open a file in write and binary mode
with open("kde_night_test.tiff", 'wb') as file:
  # Write the contents of the buffer to the file
  file.write(plot.getvalue())
