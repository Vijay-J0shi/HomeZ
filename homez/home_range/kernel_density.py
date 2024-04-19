"""
Copyright 2024 HomeZ

Kernel Density Estimation
-------------------------
"""

# Author: Adam-Al-Rahman <adam.al.rahman.dev@gmail.com>

from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt
from typing import List


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

  def estimate_density(self, confidence_level=0.95):
    xi, yi = np.meshgrid(np.linspace(min(self.x), max(self.x), int((max(self.x) - min(self.x)) / self.cell_size)),
                         np.linspace(min(self.y), max(self.y), int((max(self.y) - min(self.y)) / self.cell_size)))

    if self.bandwidth:
      kde = gaussian_kde([self.x, self.y], bw_method=self.bandwidth)
    else:
      kde = gaussian_kde([self.x, self.y], bw_method='silverman')

    zi = kde(np.vstack([xi.ravel(), yi.ravel()]))
    zi = zi.reshape(xi.shape)

    # calculate the threshold density for the specified confidence level
    sorted_density_values = np.sort(zi.ravel())
    threshold_index = int((1 - confidence_level) * len(sorted_density_values))
    threshold_density = sorted_density_values[threshold_index]

    # set density values outside the confidence interval to nan
    zi[zi < threshold_density] = np.nan

    # calculate the area within the threshold density
    area = np.nansum(zi) * self.cell_size ** 2

    return [xi, yi, zi], area

  def plot(self, estimate_density: List):
    xi, yi, zi = estimate_density
    plt.figure(figsize=(10, 10))
    plt.pcolormesh(xi, yi, zi, shading='auto')
    plt.colorbar(label='Density')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Kernel Density Estimation')

    # Capture the plot as an image (tiff format)
    from io import BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='tiff')
    buffer.seek(0)

    # Return the image buffer
    return buffer

  def calculate(self, confidence_level=0.95):
    estimate_density = self.estimate_density(confidence_level)
    plot = self.plot(estimate_density[0])
    area = estimate_density[1]
    return [area, plot]
