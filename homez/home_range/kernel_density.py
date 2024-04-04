"""
Copyright 2024 HomeZ

Kernel Density Estimation
-------------------------
"""

# Author: Adam-Al-Rahman <adam.al.rahman.dev@gmail.com>

from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt

from .utils import utils


class KernelDensityEstimator:

  def __init__(self, shapefile_path, output_raster_path, cell_size=1.0, bandwidth=None):
    self.shapefile_path = shapefile_path
    self.output_raster_path = output_raster_path
    self.cell_size = cell_size
    self.bandwidth = bandwidth

  def read_shapefile(self):
    # Read the shapefile using geopandas
    return utils.read_shapefile(self.shapefile_path)

  def estimate_density(self):
    # Read the shapefile
    gdf = self.read_shapefile()

    # Extract x and y coordinates from the shapefile
    x = gdf.x.astype(float)
    y = gdf.y.astype(float)

    # Create a 2D grid of points
    xi, yi = np.meshgrid(np.linspace(min(x), max(x), int((max(x) - min(x)) / self.cell_size)),
                         np.linspace(min(y), max(y), int((max(y) - min(y)) / self.cell_size)))

    # Estimate the kernel density with adaptive bandwidth if provided
    if self.bandwidth:
      kde = gaussian_kde([x, y], bw_method=self.bandwidth)
    else:
      kde = gaussian_kde([x, y], bw_method='silverman')

    zi = kde([xi.ravel(), yi.ravel()])

    # Reshape the density values to match the grid
    zi = zi.reshape(xi.shape)

    return [xi, yi, zi]

  def plot_density(self):
    xi, yi, zi = self.estimate_density()
    plt.figure(figsize=(10, 8))
    plt.pcolormesh(xi, yi, zi, shading='auto')
    plt.colorbar(label='Density')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Kernel Density Estimation')
    plt.savefig(self.output_raster_path, format='tif')

  def create_raster(self):
    estimate_density = self.estimate_density()
    utils.create_raster(estimate_density, self.output_raster_path, self.cell_size)
