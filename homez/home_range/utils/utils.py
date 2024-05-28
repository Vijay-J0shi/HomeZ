import geopandas as gpd
import pandas as pd
from geopy.distance import geodesic

from typing import Tuple


def read_shapefile(shapefile):
  # Read the shapefile using geopandas
  return gpd.read_file(shapefile)


def separate_day_night_coordinates(gdf, time_column="time"):
  """
    Separate a GeoDataFrame into day and night data based on a time column.

    :param gdf: GeoDataFrame with time-based data
    :param time_column: Name of the column containing time data
    :return: A tuple (day_data, night_data) of GeoDataFrames
    """
  # Convert the time column to datetime.time format using pandas
  gdf[time_column] = pd.to_datetime(gdf[time_column], format='%H:%M:%S').dt.time

  # Define the day time range
  day_start = pd.to_datetime("06:00:00", format='%H:%M:%S').time()
  day_end = pd.to_datetime("18:00:00", format='%H:%M:%S').time()

  # Function to determine if the time is day
  def is_day(time):
    return day_start <= time < day_end

  # Split the GeoDataFrame into day and night data
  day_data = gdf[gdf[time_column].apply(is_day)]
  night_data = gdf[~gdf[time_column].apply(is_day)]

  return day_data, night_data


def geodesic_distance(point_1, point_2):
  return geodesic(point_1, point_2).kilometers


def time_to_seconds(time_str):
  hours, minutes, seconds = map(int, str(time_str).split(':'))
  return (hours * 3600) + (minutes * 60) + seconds


# Function to sort GeoDataFrame rows based on time values
def sort_time_values(df, column_name):
  df['time'] = df[column_name].apply(time_to_seconds)
  sorted_df = df.sort_values(by=column_name)
  #  sorted_df.drop(columns='time', inplace=True)  # necessary to remove the total second
  return sorted_df


def homez_distance_displacement(gdf):
  # Convert to a GeoDataFrame
  gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf.Longitude, gdf.Latitude))
  results = []

  date_grouped = gdf.groupby('date')

  for date, date_group in date_grouped:
    collar_id_grouped = date_group.groupby("Collar_id")

    for collar_id, collar_id_group in collar_id_grouped:
      time_sorted_group = sort_time_values(collar_id_group, "time")
      point_1 = (time_sorted_group.Latitude.iloc[0], time_sorted_group.Longitude.iloc[0])
      point_2 = (time_sorted_group.Latitude.iloc[-1], time_sorted_group.Longitude.iloc[-1])

      displacement = geodesic_distance(point_1, point_2)

      distance = 0
      for i in range(1, len(time_sorted_group)):
        point_1 = (time_sorted_group.Latitude.iloc[i - 1], time_sorted_group.Longitude.iloc[i - 1])
        point_2 = (time_sorted_group.Latitude.iloc[i], time_sorted_group.Longitude.iloc[i])

        distance += geodesic_distance(point_1, point_2)

      results.append({"Collar_id": collar_id, "date": date, "distance": distance, "displacement": displacement})

  return results
