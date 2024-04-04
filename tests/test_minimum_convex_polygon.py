import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
  from homez.home_range.utils import utils
  from homez.home_range.minimum_convex_polygon import MinimumConvexPolygon
except ImportError as e:
  print(f"Error: import module: {e}")
  sys.exit(1)

dataset = "tests/sample.csv"

gdf = utils.read_shapefile(dataset)
print(gdf)

x = gdf.x.astype(float)
y = gdf.y.astype(float)

mcp = MinimumConvexPolygon(x, y)
mcp.plot(output_raster_path="tests/mcp_sample.tif")
