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
data = utils.read_shapefile(dataset)

print(data)

kde = KernelDensityEstimator(shapefile_path=dataset, output_raster_path="tests/sample.tif")
kde.plot_density()
