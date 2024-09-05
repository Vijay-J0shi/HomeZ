import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from homez.home_range.utils.utils import (
        homez_distance_displacement,
        read_shapefile,
        separate_day_night_coordinates,
    )
    from homez.home_range.kernel_density import KernelDensityEstimator
except ImportError as e:
    print(f"Error: import module: {e}")
    sys.exit(1)


def kde(path, bandwidth=0.95):
    if bandwidth > 1.0:
        print("ERROR: Cell size must be greater than 1.0.")
        return

    dataset = path
    gdf = read_shapefile(dataset)
    gdf.set_crs(epsg=4326, inplace=True)
    day_data, night_data = separate_day_night_coordinates(gdf, time_column="NST Time")

    day_plot = day_kde(day_data, bandwidth)
    night_plot = night_kde(night_data, bandwidth)
    return day_plot, night_plot


def day_kde(day_data, bandwidth):
    x_day = day_data.Longitude.astype(float)
    y_day = day_data.Latitude.astype(float)

    kde_day = KernelDensityEstimator(x_day, y_day, bandwidth)
    kde_day_res = kde_day.calculate()

    print(kde_day_res)

    day_plot = kde_day_res
    return day_plot


def night_kde(night_data, bandwidth):
    x_night = night_data.Longitude.astype(float)
    y_night = night_data.Latitude.astype(float)

    kde_night = KernelDensityEstimator(x_night, y_night, bandwidth)
    kde_night_res = kde_night.calculate()

    print(kde_night_res)

    night_plot = kde_night_res
    return night_plot


def dist(path):
    dataset = path
    gdf = read_shapefile(dataset)
    distance = homez_distance_displacement(gdf)
    return distance
