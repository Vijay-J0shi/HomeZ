
---

# HomeZ: Kernel Density Estimation and Minimum Convex Polygon

## Overview

This project provides implementations for Kernel Density Estimation (KDE) and Minimum Convex Polygon (MCP) algorithms. These methods are used for spatial analysis and visualization of geographical data points, offering insights into density distributions and convex boundary approximations for datasets. Both algorithms are equipped with visualization features that output results as `.tiff` images.

## Features

1. **Kernel Density Estimation (KDE)**:
   - Visualizes the density of data points using Gaussian Kernel Density Estimation.
   - Supports configurable bandwidth for kernel smoothing.
   - Generates a density plot that is saved in `.tiff` format.

2. **Minimum Convex Polygon (MCP)**:
   - Computes the convex hull that encloses a given set of points.
   - Visualizes the convex polygon and the points, and saves the result as a `.tiff` image.

## Requirements

- Python 3.x
- NumPy
- SciPy
- Matplotlib
- Pandas


## Usage

### Kernel Density Estimation (KDE)

The `KernelDensityEstimator` class estimates and plots the density of points based on their longitude and latitude coordinates.

Example usage:
```python
from kde import KernelDensityEstimator

longitude = [1, 2, 3, ...]
latitude = [4, 5, 6, ...]
bandwidth = 0.5

kde = KernelDensityEstimator(longitude, latitude, bandwidth)
image_buffer = kde.calculate()
```
This will generate a KDE plot, stored as a `.tiff` image in a buffer, which you can save to a file.

### Minimum Convex Polygon (MCP)

The `MinimumConvexPolygon` class calculates and plots the convex hull of a set of geographical points.

Example usage:
```python
from mcp import MinimumConvexPolygon
import pandas as pd

# Load sample data
data = pd.read_csv('tracking_sample.csv')
x_coords = data['x'].dropna().tolist()
y_coords = data['y'].dropna().tolist()

mcp = MinimumConvexPolygon(x_coords, y_coords, alpha=0.5)
image_buffer = mcp.plot_mcp()
```
