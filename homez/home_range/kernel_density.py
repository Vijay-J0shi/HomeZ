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

  def __init__(self, x, y, cell_size=1.0, bandwidth=None):
    """
    :param x: x coordinate of each point
    :param y: y coordinate of each point
    :param bandwidth: smooth factor
    """
    self.cell_size = cell_size
    self.bandwidth = bandwidth
    self.x = x
    self.y = y

  def estimate_density(self):

    # Create a 2D grid of points
    xi, yi = np.meshgrid(np.linspace(min(self.x), max(self.x), int((max(self.x) - min(self.x)) / self.cell_size)),
                         np.linspace(min(self.y), max(self.y), int((max(self.y) - min(self.y)) / self.cell_size)))

    # Estimate the kernel density with adaptive bandwidth if provided
    if self.bandwidth:
      kde = gaussian_kde([self.x, self.y], bw_method=self.bandwidth)
    else:
      kde = gaussian_kde([self.x, self.y], bw_method='silverman')

    zi = kde([xi.ravel(), yi.ravel()])

    # Reshape the density values to match the grid
    zi = zi.reshape(xi.shape)

    return [xi, yi, zi]

  def plot(self, output_raster_path):
    xi, yi, zi = self.estimate_density()
    plt.figure(figsize=(10, 10))
    plt.pcolormesh(xi, yi, zi, shading='auto')
    plt.colorbar(label='Density')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Kernel Density Estimation')
    plt.savefig(output_raster_path, format='tif')

  def create_raster(self, output_raster_path):
    estimate_density = self.estimate_density()
    utils.create_raster(estimate_density, output_raster_path, self.cell_size)
