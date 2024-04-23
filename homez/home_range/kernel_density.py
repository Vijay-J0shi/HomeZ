"""
Copyright 2024 HomeZ

Kernel Density Estimation
-------------------------
"""

# Author: Adam-Al-Rahman <adam.al.rahman.dev@gmail.com>

from scipy.stats import gaussian_kde
from scipy.integrate import dblquad  # Importing double integration for 2D data
import numpy as np
import matplotlib.pyplot as plt
from typing import List


class KernelDensityEstimator:

  def __init__(self, x, y, cell_size=1.0):
    """
    :param x: x coordinate of each point
    :param y: y coordinate of each point
    :param bandwidth: smooth factor
    """
    self.cell_size = cell_size
    self.x = x
    self.y = y

  def estimate_density(self, bandwidth=None):
    xi, yi = np.meshgrid(np.linspace(min(self.x), max(self.x), int((max(self.x) - min(self.x)) / self.cell_size)),
                         np.linspace(min(self.y), max(self.y), int((max(self.y) - min(self.y)) / self.cell_size)))

    if bandwidth:
      kde = gaussian_kde([self.x, self.y], bw_method=bandwidth)
    else:
      kde = gaussian_kde([self.x, self.y], bw_method='silverman')

    zi = kde(np.vstack([xi.ravel(), yi.ravel()]))
    zi = zi.reshape(xi.shape)

    # Define the integration limits (based on your data range)
    lower_limit_x = min(self.x)
    upper_limit_x = max(self.x)
    lower_limit_y = min(self.y)
    upper_limit_y = max(self.y)

    # Integrate the KDE along both dimensions
    area, _ = dblquad(lambda x, y: kde.evaluate([self.x, self.y])[0], lower_limit_x, upper_limit_x, lower_limit_y,
                      upper_limit_y)

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

  def calculate(self, bandwidth=0.95):
    estimate_density = self.estimate_density(bandwidth)
    plot = self.plot(estimate_density[0])
    area = estimate_density[1]
    return [area, plot]
