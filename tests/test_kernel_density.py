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
print(gdf)

x = gdf.geometry.x.astype(float)
y = gdf.y.astype(float)

kde = KernelDensityEstimator(x, y)
kde.plot(output_raster_path="tests/kde_sample.tif")
kde.create_raster("kde_sample.tif")
