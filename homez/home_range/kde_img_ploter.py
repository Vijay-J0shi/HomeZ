import sys
import numpy as np
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import traceback

try:
    from utils.utils import (
        homez_distance_displacement,
        read_shapefile,
        separate_day_night_coordinates,
    )
    from kernel_density import KernelDensityEstimator
except ImportError as e:
    print(f"Error: import module: {e}", flush=True)
    sys.exit(1)

def kde(path, bandwidth=0.95):
    if bandwidth > 1.0:
        print("ERROR: Bandwidth must be greater than 1.0.", flush=True)
        sys.exit(1)
    if bandwidth <= 0:
        print("ERROR: Bandwidth must be positive.", flush=True)
        sys.exit(1)

    print(f"Checking file: {path}", flush=True)
    if not os.path.exists(path):
        print(f"File not found: {path}", flush=True)
        sys.exit(1)

    try:
        print("Reading shapefile...", flush=True)
        gdf = read_shapefile(path)
        gdf.set_crs(epsg=4326, inplace=True)
        print(f"Shapefile loaded, rows: {len(gdf)}, columns: {gdf.columns.tolist()}", flush=True)
    except Exception as e:
        print(f"Error reading shapefile: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    try:
        print("Separating day/night coordinates...", flush=True)
        day_data, night_data = separate_day_night_coordinates(gdf, time_column="NST Time")
        print(f"Day data rows: {len(day_data)}, Night data rows: {len(night_data)}", flush=True)
    except Exception as e:
        print(f"Error in day/night split: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    try:
        print("Computing day KDE...", flush=True)
        day_plot = day_kde(day_data, bandwidth)
        print("Computing night KDE...", flush=True)
        night_plot = night_kde(night_data, bandwidth)
        print(f"KDE returning: {day_plot}, {night_plot}", flush=True)
        return day_plot, night_plot
    except Exception as e:
        print(f"Error in KDE computation: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

def day_kde(day_data, bandwidth):
    try:
        print("Extracting day coordinates...", flush=True)
        x_day = day_data.Longitude.astype(float)
        y_day = day_data.Latitude.astype(float)
        print(f"Day points: {len(x_day)}", flush=True)

        # Check for NaNs or invalid values
        if x_day.isna().any() or y_day.isna().any():
            print("Error: NaN values in day coordinates", flush=True)
            sys.exit(1)
        if not (x_day.apply(lambda x: isinstance(x, (int, float))).all() and
                y_day.apply(lambda x: isinstance(x, (int, float))).all()):
            print("Error: Non-numeric values in day coordinates", flush=True)
            sys.exit(1)

        if len(x_day) < 2:
            print("Error: Need at least 2 points for KDE", flush=True)
            sys.exit(1)

        print("Initializing KernelDensityEstimator...", flush=True)
        kde_day = KernelDensityEstimator(x_day, y_day, bandwidth)
        print("Calculating day KDE...", flush=True)
        kde_day_res = kde_day.calculate()
        print(f"Day KDE result type: {type(kde_day_res)}", flush=True)

        # Check if result is a BytesIO buffer
        if not isinstance(kde_day_res, BytesIO):
            print(f"Error: Expected BytesIO buffer, got {type(kde_day_res)}", flush=True)
            sys.exit(1)

        # Verify buffer is not empty
        kde_day_res.seek(0)
        buffer_size = len(kde_day_res.read())
        kde_day_res.seek(0)  # Reset buffer position
        if buffer_size == 0:
            print("Error: Day KDE buffer is empty", flush=True)
            sys.exit(1)
        print(f"Day KDE buffer size: {buffer_size}", flush=True)

        return kde_day_res
    except Exception as e:
        print(f"Error in day_kde: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

def night_kde(night_data, bandwidth):
    try:
        print("Extracting night coordinates...", flush=True)
        x_night = night_data.Longitude.astype(float)
        y_night = night_data.Latitude.astype(float)
        print(f"Night points: {len(x_night)}", flush=True)

        # Check for NaNs or invalid values
        if x_night.isna().any() or y_night.isna().any():
            print("Error: NaN values in night coordinates", flush=True)
            sys.exit(1)
        if not (x_night.apply(lambda x: isinstance(x, (int, float))).all() and
                y_night.apply(lambda x: isinstance(x, (int, float))).all()):
            print("Error: Non-numeric values in night coordinates", flush=True)
            sys.exit(1)

        if len(x_night) < 2:
            print("Error: Need at least 2 points for KDE", flush=True)
            sys.exit(1)

        print("Initializing KernelDensityEstimator...", flush=True)
        kde_night = KernelDensityEstimator(x_night, y_night, bandwidth)
        print("Calculating night KDE...", flush=True)
        kde_night_res = kde_night.calculate()
        print(f"Night KDE result type: {type(kde_night_res)}", flush=True)

        # Check if result is a BytesIO buffer
        if not isinstance(kde_night_res, BytesIO):
            print(f"Error: Expected BytesIO buffer, got {type(kde_night_res)}", flush=True)
            sys.exit(1)

        # Verify buffer is not empty
        kde_night_res.seek(0)
        buffer_size = len(kde_night_res.read())
        kde_night_res.seek(0)  # Reset buffer position
        if buffer_size == 0:
            print("Error: Night KDE buffer is empty", flush=True)
            sys.exit(1)
        print(f"Night KDE buffer size: {buffer_size}", flush=True)

        return kde_night_res
    except Exception as e:
        print(f"Error in night_kde: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

def dist(path):
    try:
        print(f"Computing distance for {path}...", flush=True)
        gdf = read_shapefile(path)
        distance = homez_distance_displacement(gdf)
        print(f"Distance: {distance}", flush=True)
        return distance
    except Exception as e:
        print(f"Error in dist: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    file_path = r"D:/College_Projects/HomeZ/Sample data/kano atiq.csv"
    print(os.path.exists(file_path), flush=True)
    bandwidth = 0.5
    print(f"Starting KDE calculation with bandwidth {bandwidth}...", flush=True)
    try:
        day_kde, night_kde = kde(file_path, bandwidth)
        print("KDE success - Day buffer:", day_kde, "Night buffer:", night_kde, flush=True)
        day_kde.seek(0)
        night_kde.seek(0)
        print("Day KDE buffer size:", len(day_kde.read()), flush=True)
        print("Night KDE buffer size:", len(night_kde.read()), flush=True)
    except Exception as e:
        print(f"Main block error: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)