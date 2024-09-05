"""
Copyright 2024 HomeZ
Kernel Density Estimation
-------------------------
"""

# Author: Adam-Al-Rahman <adam.al.rahman.dev@gmail.com>

import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from io import BytesIO
from typing import List


class KernelDensityEstimator:
    def __init__(self, longitude, latitude, bandwidth):
        """
        :param longitude: longitude coordinate of each point
        :param latitude: latitude coordinate of each point
        """
        self.x = longitude
        self.y = latitude
        self.bandwidth = bandwidth

    def estimate_density(self, bandwidth=None):
        # Generate a grid over which to evaluate the KDE
        xi, yi = np.meshgrid(
            np.linspace(min(self.x), max(self.x), 100),
            np.linspace(min(self.y), max(self.y), 100),
        )

        if bandwidth:
            kde = gaussian_kde([self.x, self.y], bw_method=bandwidth)
        else:
            kde = gaussian_kde([self.x, self.y], bw_method="silverman")

        zi = kde([xi.ravel(), yi.ravel()])
        zi = zi.reshape(xi.shape)

        return [xi, yi, zi]

    def plot(self, estimate_density: List):
        xi, yi, zi = estimate_density
        plt.figure(figsize=(10, 10))
        plt.pcolormesh(xi, yi, zi, shading="auto")
        plt.colorbar(label="Density")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Kernel Density Estimation")

        # Capture the plot as an image (tiff format)
        buffer = BytesIO()
        plt.savefig(buffer, format="tiff")
        buffer.seek(0)

        plt.close()

        # Return the image buffer
        return buffer

    def calculate(self, bandwidth=0.5):
        bandwidth = self.bandwidth
        estimate_density = self.estimate_density(bandwidth)
        plot = self.plot(estimate_density)
        return plot
