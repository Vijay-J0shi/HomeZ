
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

Install dependencies using:
```bash
pip install numpy scipy matplotlib pandas
```

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


# Minimum Convex Polygon (MCP) for Animal Home Range Estimation

This project implements a Minimum Convex Polygon (MCP) algorithm, commonly used in ecology to estimate the home range of animals based on geographical coordinates. The MCP is computed using convex hulls of geographic points, with confidence intervals and area calculations provided.

## Usage

### Input Data
The MCP algorithm requires a dataset containing longitude and latitude values, typically stored in a shapefile. The dataset must contain at least the following fields:
- `Longitude`: X-coordinates
- `Latitude`: Y-coordinates
- `NST Time`: A timestamp or datetime column (used for day/night separation).

### Running the MCP Function
The main function `MCP` runs the MCP algorithm and returns the areas for total, day, and night ranges, as well as visual representations.

```python
from mcp import MCP

image_buffer_day, image_buffer_night, area_day, area_night, area_total = MCP(path_to_shapefile, alpha=0.5, conf_lvl=95)
```

#### Parameters:
- `path_to_shapefile`: Path to the input shapefile.
- `alpha`: Transparency level for the plotted polygons.
- `conf_lvl`: Confidence level (percentage) for the polygon area to be plotted.

### Output
The `MCP` function returns:
1. **image_buffer_day**: A `BytesIO` buffer containing the MCP plot for daytime points.
2. **image_buffer_night**: A `BytesIO` buffer containing the MCP plot for nighttime points.
3. **area_day**: The area of the daytime MCP polygon in square kilometers.
4. **area_night**: The area of the nighttime MCP polygon in square kilometers.
5. **area_total**: The total area of the MCP polygon for all points in square kilometers.


### Example Output:

The MCP algorithm will generate plots like the following for day and night coordinates:

- Minimum Convex Polygon with a confidence level of 95% for daytime and nighttime data points.
- The calculated area (in square kilometers) for both day, night, and total range.

## Methods

### `mcp_algorithm(self, points)`
Calculates the convex hull using the points (longitude, latitude). It constructs the upper and lower hulls to form the Minimum Convex Polygon.

### `plot_mcp(self, confidence_level)`
Plots the MCP based on a specific confidence level. It fills the area enclosed by the polygon and returns the plot as a `BytesIO` object and the area.

### `calculate_area(self, convex_hull)`
Uses the Shoelace formula to calculate the area of the convex polygon (in square kilometers). This method also accounts for geographic distances.

## Dependencies

This project requires the following Python libraries:

- `pandas`: Used for data handling.
- `matplotlib`: Used for plotting the MCP polygons.
- `numpy`: Used for numeric calculations.
- `BytesIO`: To store plot outputs in memory as buffer objects.

Additionally, the `utils` module (external to this project) is required for:
- Reading shapefiles (`utils.read_shapefile`).
- Separating day and night points (`separate_day_night_coordinates`).

# Kernel Density Estimation (KDE) and Distance Displacement Calculation

```markdown

This project provides a Python application that performs Kernel Density Estimation (KDE) and distance displacement calculations for geospatial data. The project includes utilities for visualizing KDE plots for day and night time data and calculating home range displacements using shapefiles.

Additionally, you must have the `utils` module which includes functions such as:
- `homez_distance_displacement`: Calculates distance displacement for geospatial data.
- `read_shapefile`: Reads the input shapefile data.
-'separate_day_night_coordinates`: Splits the data into day and night based on time column.
-`KernelDensityEstimator`: A class for KDE calculation.

## Usage

### Input Data

The application expects a dataset (typically a shapefile) that contains geospatial points, with the following attributes:
- `Longitude`: X-coordinate of the geographic points.
-`Latitude`: Y-coordinate of the geographic points.
 `NST Time`: Timestamp for each data point used for separating day and night points.

### KDE Function

The `kde` function performs Kernel Density Estimation on both day and night time data from the shapefile.

#### Parameters:
 `path`: Path to the shapefile containing geospatial data.
`bandwidth`: Bandwidth for the KDE algorithm. It controls the smoothing of the KDE plot. Must be less than or equal to 1.0.

#### Example:

```python
from kde import kde

day_plot, night_plot = kde('path_to_shapefile', bandwidth=0.95)
```

### Distance Displacement Function

 The `dist` function calculates the displacement or movement distance for geospatial data points.


## Methods

### `kde(path, bandwidth=0.95)`

This function reads the shapefile and separates the day and night coordinates, then runs the KDE algorithm for both subsets of data.

### `day_kde(day_data, bandwidth)`
Runs the KDE algorithm on daytime data points using the specified bandwidth and returns the resulting density plot.

### `night_kde(night_data, bandwidth)`
Runs the KDE algorithm on nighttime data points using the specified bandwidth and returns the resulting density plot.

### `dist(path)`
Calculates the total displacement of the data points from the shapefile using the `homez_distance_displacement` function.

## Dependencies

This project depends on the following Python libraries:

 `PyQt6`: Used for building the GUI for the application.
`pandas`: For data handling and manipulation.
 `numpy`: For numeric computations.
 `matplotlib`: For plotting KDE visualizations.
`Pillow`: For image manipulation using `Image` class.
