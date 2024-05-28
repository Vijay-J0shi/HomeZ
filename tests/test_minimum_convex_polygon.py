import numpy as np
import geopandas as gpd
from shapely.geometry import MultiPoint, Point
import matplotlib.pyplot as plt


def calculate_mcp(points):
  """
    Calculate the Minimum Convex Polygon (MCP) for a set of 2D points (longitude, latitude).
    Parameters:
        points (np.array): 2D array where each row is a data point [longitude, latitude].
    Returns:
        shapely.geometry.Polygon: The MCP polygon.
    """
  # Create a MultiPoint object from the points
  multipoint = MultiPoint(points)

  # Calculate the convex hull (MCP)
  mcp = multipoint.convex_hull

  return mcp


def plot_mcp(points, mcp):
  """
    Plot the points and their Minimum Convex Polygon (MCP).
    Parameters:
        points (np.array): 2D array where each row is a data point [longitude, latitude].
        mcp (shapely.geometry.Polygon): The MCP polygon.
    """
  # Convert points to GeoDataFrame
  gdf_points = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y in points], crs='EPSG:4326')

  # Plot points
  fig, ax = plt.subplots()
  gdf_points.plot(ax=ax, color='blue', markersize=5, label='Points')

  # Plot MCP
  gpd.GeoSeries([mcp], crs='EPSG:4326').plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2, label='MCP')

  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.title('Minimum Convex Polygon (MCP)')
  plt.legend()
  plt.show()


def calculate_area_mcp(mcp, crs_from='EPSG:4326', crs_to='ESRI:54009'):
  """
    Calculate the area of the MCP in square kilometers using a given projection.
    Parameters:
        mcp (shapely.geometry.Polygon): The MCP polygon.
        crs_from (str): The CRS of the input coordinates (default 'EPSG:4326' for WGS84).
        crs_to (str): The CRS to transform the coordinates to (default 'ESRI:54009' for World Mollweide).
    Returns:
        float: The area of the MCP in square kilometers.
    """
  # Convert the MCP to a GeoSeries and set the CRS
  mcp_gdf = gpd.GeoSeries([mcp], crs=crs_from)

  # Transform the MCP coordinates to the new projection
  mcp_projected = mcp_gdf.to_crs(crs_to)

  # Calculate the area in square meters
  area_sqm = mcp_projected.area[0]

  # Convert the area to square kilometers
  area_sqkm = area_sqm / 1e6

  return area_sqkm


# Example usage
if __name__ == "__main__":
  # Generate some random longitude and latitude data
  np.random.seed(0)
  longitude = np.random.uniform(-100, -90, 100)
  latitude = np.random.uniform(40, 50, 100)
  points = np.column_stack((longitude, latitude))

  # Calculate the MCP
  mcp = calculate_mcp(points)
  print("MCP Coordinates:", mcp)

  # Plot the points and MCP
  plot_mcp(points, mcp)

  # Calculate the area of the MCP
  area = calculate_area_mcp(mcp)
  print(f"Area of the MCP: {area:.2f} square kilometers")
