"""

Copyright 2024 HomeZ
Kernel Density Estimation
-------------------------
"""

# Author: Adam-Al-Rahman <adam.al.rahman.dev@gmail.com>

from typing import List

import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from scipy.stats import gaussian_kde


class KernelDensityEstimator:

  def __init__(self, latitude: List[float], longitude: List[float]):
    """
    :param latitude: x coordinate of each point
    :param longitude: y coordinate of each point
    :param bandwidth: smooth factor
    """

    # Create a GeoDataFrame from the points
    geometry = [Point(lon, lat) for lon, lat in zip(longitude, latitude)]
    gdf = gpd.GeoDataFrame(geometry=geometry, crs='EPSG:4326')

    # Extract latitude and longitude coordinates
    self.latitude = gdf.geometry.latitude
    self.longitude = gdf.geometry.longitude

    # Ensure the CSV has 'longitude' and 'latitude' columns not empty
    if not self.latitude and not self.longitude:
      raise ValueError("CSV must contain 'longitude' and 'latitude' columns")
    elif not self.latitude:
      raise ValueError("CSV must contain 'latitude' columns")
    elif not self.longitude:
      raise ValueError("CSV must contain 'longitude' columns")

  def estimate_density(self, bandwidth=None):
    dataset = np.vstack([self.latitude, self.longitude])
    if bandwidth:
      kde = gaussian_kde(dataset, bw_method=bandwidth)
    else:
      kde = gaussian_kde(dataset, bw_method='silverman')

    # Create grid to evaluate kde
    lat_min, lat_max = min(self.latitude) - 1, max(self.latitude) + 1
    lon_min, lon_max = min(self.longitude) - 1, max(self.longitude) + 1
    X, Y = np.mgrid[lon_min:lon_max:100j, lat_min:lat_max:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kde(positions).T, X.shape)

    return [Z, lat_min, lat_max, lon_min, lon_max]

  def plot(self, estimate_density):
    Z, lat_min, lat_max, lon_min, lon_max = estimate_density
    _, ax = plt.subplots()
    ax.imshow(np.rot90(Z), cmap="viridis", extent=[lon_min, lon_max, lat_min, lat_max])
    ax.plot(self.longitude, self.latitude, 'k.', markersize=2)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Kernel Density Estimation')

    # Capture the plot as an image (tiff format)
    from io import BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='tiff')
    buffer.seek(0)

    # Return the image buffer
    return buffer

  def calculate(self, bandwidth=None):
    return self.plot(self.estimate_density(bandwidth))
