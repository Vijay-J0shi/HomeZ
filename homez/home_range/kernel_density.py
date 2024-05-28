"""
Copyright 2024 HomeZ
Kernel Density Estimation
-------------------------
"""

# Author: Adam-Al-Rahman <adam.al.rahman.dev@gmail.com>

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from io import BytesIO


class KernelDensityEstimator:

  def __init__(self, longitude, latitude):
    """
    :param latitude: x coordinate of each point
    :param longitude: y coordinate of each point
    """
    self.longitude = longitude
    self.latitude = latitude

  # def add_noise(self, data, noise_level=1e-6):
  #   """
  #   Adds a small amount of noise to the data to avoid singular covariance matrix issues.
  #   :param data: Original data
  #   :param noise_level: Magnitude of the noise to add
  #   :return: Data with added noise
  #   """
  #   noise = noise_level * np.random.randn(*data.shape)
  #   return data + noise

  def estimate_density(self, bandwidth=None):
    dataset = np.vstack([self.latitude, self.longitude])

    # # Add noise to the dataset to avoid singular covariance matrix issues
    # dataset = self.add_noise(dataset)

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
    buffer = BytesIO()
    plt.savefig(buffer, format='tiff')
    buffer.seek(0)

    # Return the image buffer
    return buffer

  def calculate(self, bandwidth=None):
    return self.plot(self.estimate_density(bandwidth))
