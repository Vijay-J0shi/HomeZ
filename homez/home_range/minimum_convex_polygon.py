import os
import sys
import traceback
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from io import BytesIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
try:
    from utils import utils, separate_day_night_coordinates
except ImportError as e:
    print(f"Import error: {e}", flush=True)
    sys.exit(1)

class MinimumConvexPolygon:
    def __init__(self, x_cord, y_cord, alpha):
        self.x_coords = x_cord
        self.y_coords = y_cord
        self.alpha = alpha
        self.points = list(zip(x_cord, y_cord))

    def mcp_algorithm(self, points):
        if len(points) < 3:
            print("Error: Need at least 3 points for convex hull", flush=True)
            sys.exit(1)
        points = sorted(points)
        upper_hull = []
        lower_hull = []
        for p in points:
            while len(upper_hull) >= 2 and self.cross_product(upper_hull[-2], upper_hull[-1], p) <= 0:
                upper_hull.pop()
            upper_hull.append(p)
        for p in reversed(points):
            while len(lower_hull) >= 2 and self.cross_product(lower_hull[-2], lower_hull[-1], p) <= 0:
                lower_hull.pop()
            lower_hull.append(p)
        return upper_hull[:-1] + lower_hull[:-1]

    def cross_product(self, o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def plot_mcp(self, confidence_level):
        print(f"Plotting MCP for {confidence_level}% confidence", flush=True)
        fig, ax = plt.subplots(figsize=(10, 10))
        num_points = int(len(self.x_coords) * (confidence_level / 100))
        sampled_points = list(zip(self.x_coords, self.y_coords))[:num_points]
        convex_hull = self.mcp_algorithm(sampled_points)
        x, y = zip(*convex_hull)
        ax.fill(x, y, alpha=self.alpha, label=f"{confidence_level}% Confidence Interval")
        ax.scatter(self.x_coords, self.y_coords, color="black", s=5, label="Points")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.title("Minimum Convex Polygon with Confidence Interval")
        plt.legend()
        area_square_units = self.calculate_area(convex_hull)
        buffer = BytesIO()
        plt.savefig(buffer, format="tiff")
        buffer.seek(0)
        plt.close()
        print(f"Plot buffer size: {len(buffer.getvalue())}", flush=True)
        return buffer, area_square_units

    def calculate_area(self, convex_hull):
        n = len(convex_hull)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += convex_hull[i][0] * convex_hull[j][1]
            area -= convex_hull[j][0] * convex_hull[i][1]
        return abs(area) / 2.0 * (111.32**2) / 2

def MCP(path, alpha, conf_lvl):
    print(f"Checking file: {path}", flush=True)
    if not os.path.exists(path):
        print(f"File not found: {path}", flush=True)
        sys.exit(1)
    
    print("Reading shapefile...", flush=True)
    try:
        gdf = utils.read_shapefile(path)
        print(f"Shapefile loaded, rows: {len(gdf)}, columns: {gdf.columns.tolist()}", flush=True)
    except Exception as e:
        print(f"Error reading shapefile: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    try:
        x_coords = [float(x) for x in gdf["Longitude"].tolist()]
        y_coords = [float(lat) for lat in gdf["Latitude"].tolist()]  # Fixed typo here
        print(f"Total points: {len(x_coords)}", flush=True)
        total = MinimumConvexPolygon(x_coords, y_coords, alpha)
        hull = total.mcp_algorithm(total.points)
        print(f"Total hull points: {len(hull)}", flush=True)
        image_buffer, area_total = total.plot_mcp(conf_lvl)
        print(f"Total buffer size: {len(image_buffer.getvalue())}", flush=True)

        gdf = gdf.dropna(subset=["Longitude", "Latitude"])
        print("Separating day/night coordinates...", flush=True)
        day_data, night_data = separate_day_night_coordinates(gdf, time_column="NST Time")
        print(f"Day data rows: {len(day_data)}, Night data rows: {len(night_data)}", flush=True)
        x_coords_day = [float(x) for x in day_data["Longitude"].tolist()]
        y_coords_day = [float(lat) for lat in day_data["Latitude"].tolist()]  # Consistent variable naming
        print(f"Day points: {len(x_coords_day)}", flush=True)
        mcp_day = MinimumConvexPolygon(x_coords_day, y_coords_day, alpha)
        hull_day = mcp_day.mcp_algorithm(mcp_day.points)
        image_buffer_day, area_day = mcp_day.plot_mcp(conf_lvl)
        print(f"Day buffer size: {len(image_buffer_day.getvalue())}", flush=True)
        x_coords_night = [float(x) for x in night_data["Longitude"].tolist()]
        y_coords_night = [float(lat) for lat in night_data["Latitude"].tolist()]  # Consistent variable naming
        print(f"Night points: {len(x_coords_night)}", flush=True)
        mcp_night = MinimumConvexPolygon(x_coords_night, y_coords_night, alpha)
        hull_night = mcp_night.mcp_algorithm(mcp_night.points)
        image_buffer_night, area_night = mcp_night.plot_mcp(conf_lvl)
        print(f"Night buffer size: {len(image_buffer_night.getvalue())}", flush=True)
        area_night = round(area_night, 3)
        area_day = round(area_day, 3)
        area_total = round(area_total, 3)
        return image_buffer_day, image_buffer_night, area_day, area_night, area_total
    except Exception as e:
        print(f"Error in MCP: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

