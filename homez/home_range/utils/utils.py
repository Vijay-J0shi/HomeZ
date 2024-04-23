import geopandas as gpd
import pandas as pd
import geopy.distance
import rasterio
from rasterio.transform import from_origin


def read_shapefile(shapefile):
  # Read the shapefile using geopandas
  return gpd.read_file(shapefile)


def separate_day_night_coordinates(gdf, time_column="time"):
  """
  :param gdf: dataset
  :param time_column: time column name
  """

  # Convert the time column to datetime format using pandas
  gdf[time_column] = pd.to_datetime(gdf[time_column])

  # Split the GeoDataFrame into day (AM) and night (PM) data
  day_data = gdf[gdf[time_column].dt.strftime('%p') == 'AM']
  night_data = gdf[gdf[time_column].dt.strftime('%p') == 'PM']

  return (day_data, night_data)


def calculate_travel_distance(data, time_column="time", coords=("lat", "lon")):
  day_data, night_data = separate_day_night_coordinates(data, time_column)

  # Calculate the travel distance for day and night
  day_distance = sum(
    geopy.distance.distance(day_data.iloc[i][coords], day_data.iloc[i + 1][coords]).km
    for i in range(len(day_data) - 1))
  night_distance = sum(
    geopy.distance.distance(night_data.iloc[i][coords], night_data.iloc[i + 1][coords]).km
    for i in range(len(night_data) - 1))

  return day_distance, night_distance


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
