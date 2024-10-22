# Utils: Utility Functions for Spatial Analysis

## Overview

This folder contains utility functions that assist in various spatial analysis tasks. These utilities include reading shapefiles, separating day and night coordinates, calculating distances and displacements, and sorting time values in a geographical dataset.

## Contents

1. **`read_shapefile()`**:
   - Reads a shapefile and converts it into a GeoDataFrame using `geopandas`.
   - **Input**: Path to a shapefile.
   - **Output**: A `GeoDataFrame` containing the shapefile data.
   
2. **`separate_day_night_coordinates()`**:
   - Splits geographical data into day and night based on the time of day.
   - **Input**: 
     - `gdf`: A `GeoDataFrame` containing time-based data.
     - `time_column`: The column containing time data (default is `"time"`).
   - **Output**: A tuple containing two `GeoDataFrames`: `day_data` and `night_data`.

3. **`geodesic_distance()`**:
   - Calculates the geodesic distance between two geographical points (longitude, latitude).
   - **Input**: Two points in the format `(latitude, longitude)`.
   - **Output**: Distance between the points in kilometers.

4. **`time_to_seconds()`**:
   - Converts a time string (`"HH:MM:SS"`) into total seconds.
   - **Input**: A time string.
   - **Output**: Total time in seconds.

5. **`sort_time_values()`**:
   - Sorts rows of a `GeoDataFrame` based on a time column after converting the time to seconds.
   - **Input**: 
     - `df`: The `GeoDataFrame` to be sorted.
     - `column_name`: The name of the time column.
   - **Output**: A sorted `GeoDataFrame`.

6. **`homez_distance_displacement()`**:
   - Calculates the total distance traveled and displacement for each unique `Collar_id` in the dataset over time, grouped by date.
   - **Input**: A `GeoDataFrame` containing `Longitude`, `Latitude`, and `NST Time` columns.
   - **Output**: A list of dictionaries with keys:
     - `Collar_id`
     - `date`
     - `distance`: Total distance traveled (in kilometers).
     - `displacement`: Straight-line distance between the start and end points.

## Requirements

- Python 3.x
- GeoPandas
- Pandas
- Geopy

Install the required packages using:
```bash
pip install geopandas pandas geopy
```

## Usage

### Example: Reading a Shapefile and Splitting Day/Night Coordinates

```python
from utils import read_shapefile, separate_day_night_coordinates

# Load shapefile
gdf = read_shapefile("path/to/shapefile.shp")

# Split into day and night coordinates
day_data, night_data = separate_day_night_coordinates(gdf, time_column="time")
```

### Example: Calculating Distance and Displacement

```python
from utils import homez_distance_displacement
import pandas as pd

# Load a GeoDataFrame with the necessary columns
gdf = pd.read_csv("path/to/data.csv")

# Calculate distance and displacement
results = homez_distance_displacement(gdf)

for result in results:
    print(f"Collar ID: {result['Collar_id']}, Date: {result['date']}, "
          f"Distance: {result['distance']} km, Displacement: {result['displacement']} km")
```

## License

This project is licensed under the MIT License.
