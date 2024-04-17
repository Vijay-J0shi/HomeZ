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
  from homez.home_range.utils import utils
  from homez.home_range.kernel_density import KernelDensityEstimator
except ImportError as e:
  print(f"Error: import module: {e}")
  sys.exit(1)

dataset = "tests/sample.csv"

gdf = utils.read_shapefile(dataset)
gdf = gdf.dropna(subset=["x", "y"])
print(gdf)

x = gdf.x.astype(float)
y = gdf.y.astype(float)

kde = KernelDensityEstimator(x, y)
kde_result = kde.calculate(0.5)

print(kde_result[0])
