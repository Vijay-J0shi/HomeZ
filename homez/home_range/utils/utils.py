import geopandas as gpd
import rasterio
from rasterio.transform import from_origin


def read_shapefile(shapefile):
  # Read the shapefile using geopandas
  return gpd.read_file(shapefile)


def create_raster(estimate_density, output_raster_path, cell_size):
  # Estimate density
  xi, yi, zi = estimate_density

  # Get the bounding box ( xmin, xmax, ymin, ymax )
  xmin, _, _, ymax = xi.min(), yi.min(), xi.max(), yi.max()

  # Create a raster
  transform = from_origin(xmin, ymax, cell_size, cell_size)
  profile = {
    'driver': 'GTiff',
    'height': zi.shape[0],
    'width': zi.shape[1],
    'count': 1,
    'dtype': 'float32',
    'crs': 'EPSG:4326',
    'transform': transform}

  with rasterio.open(output_raster_path, 'w', **profile) as dst:
    dst.write(zi, 1)

  print(f"Raster file saved as {output_raster_path}")
