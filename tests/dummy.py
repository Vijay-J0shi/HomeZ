# import pandas as pd
# import matplotlib.pyplot as plt
# from shapely.geometry import Polygon
# from io import BytesIO

# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# try:
#     from homez.home_range.utils import utils, separate_day_night_coordinates
# except ImportError as e:
#     print(f"Error: import module: {e}")


# class MinimumConvexPolygon:
#     def __init__(self, x_coords, y_coords, alpha):
#         self.x_coords = x_coords
#         self.y_coords = y_coords
#         self.alpha = alpha

#     def mcp_algorithm(self, x_coords, y_coords):
#         points = sorted(zip(x_coords, y_coords))

#         upper_hull = []
#         lower_hull = []

#         # Compute upper hull
#         for p in points:
#             while (
#                 len(upper_hull) >= 2
#                 and self.cross_product(upper_hull[-2], upper_hull[-1], p) <= 0
#             ):
#                 upper_hull.pop()
#             upper_hull.append(p)

#         # Compute lower hull
#         for p in reversed(points):
#             while (
#                 len(lower_hull) >= 2
#                 and self.cross_product(lower_hull[-2], lower_hull[-1], p) <= 0
#             ):
#                 lower_hull.pop()
#             lower_hull.append(p)

#         # Combine upper and lower hulls to form the convex hull
#         convex_hull = upper_hull[:-1] + lower_hull[:-1]
#         return convex_hull

#     def cross_product(self, o, a, b):
#         return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

#     def plot_mcp(self, confidence_level):
#         fig, ax = plt.subplots(figsize=(10, 10))

#         sampled_points = list(zip(self.x_coords, self.y_coords))[
#             : int(len(self.x_coords) * confidence_level / 100)
#         ]
#         convex_hull = self.mcp_algorithm(self.x_coords, self.y_coords)
#         x, y = zip(*convex_hull)
#         ax.fill(
#             x, y, alpha=self.alpha, label=f"{confidence_level}% Confidence Interval"
#         )

#         ax.scatter(self.x_coords, self.y_coords, color="black", s=5, label="Points")
#         plt.xlabel("Longitude")
#         plt.ylabel("Latitude")
#         plt.title("Minimum Convex Polygon with Confidence Interval")
#         plt.legend()

#         # Calculate area of MCP for the specified confidence level
#         area_square_km = self.calculate_area(convex_hull) * (confidence_level / 100)
#         print(
#             f"Area of the Minimum Convex Polygon for {confidence_level}% confidence interval (square kilometers): {area_square_km:.6f}"
#         )

#         # Save plot as tif image
#         buffer = BytesIO()
#         plt.savefig(buffer, format="tiff")
#         buffer.seek(0)
#         # plt.show()
#         plt.close()

#         return convex_hull

#     def calculate_area(self, convex_hull):
#         poly = Polygon(convex_hull)
#         return poly.area * (
#             111.32**2
#         )  # Approximate conversion factor for latitude and longitude to kilometers


# def MCP(path, alpha, conf_lvl):
#     dataset = path
#     gdf = utils.read_shapefile(dataset)
#     gdf = gdf.dropna(subset=["x", "y"])
#     day_data, night_data = separate_day_night_coordinates(gdf, time_column="time")
#     x_coords_day = [float(x) for x in day_data["x"].tolist()]
#     y_coords_day = [float(y) for y in day_data["y"].tolist()]
#     mcp_day = MinimumConvexPolygon(x_coords_day, y_coords_day, alpha)
#     hull_day = mcp_day.mcp_algorithm(x_coords_day, y_coords_day)
#     x_coords_night = [float(x) for x in night_data["x"].tolist()]
#     y_coords_night = [float(y) for y in night_data["y"].tolist()]
#     print(len(x_coords))
#     mcp_night = MinimumConvexPolygon(x_coords_night, y_coords_night, alpha)
#     hull_night = mcp_night.mcp_algorithm(x_coords_night, y_coords_night)
#     image_buffer_day = mcp_day.plot_mcp(conf_lvl)
#     image_buffer_night = mcp_night.plot_mcp(conf_lvl)
#     area_day = mcp_day.calculate_area(hull_day)
#     area_night = mcp_night.calculate_area(hull_night)
#     print("Area of the Minimum Convex Polygon (day) (square kilometers):", area_day)
#     print("Area of the Minimum Convex Polygon (night) (square kilometers):", area_night)
#     return (
#         image_buffer_day,
#         image_buffer_night,
#         area_day,
#         area_night,
#     )


# # Read latitude and longitude values from the CSV file
# csv_file = r"C:\Users\97597\OneDrive\Desktop\kano.csv"  # Update with your CSV file path
# df = pd.read_csv(csv_file)
# x_coords = df["x"].tolist()
# y_coords = df["y"].tolist()


# for i in range(0, 2):
#     # Prompt user to input confidence level
#     confidence_level = int(input("Enter the confidence level (0-100): "))

#     mcp = MinimumConvexPolygon(x_coords, y_coords, alpha=0.5)
#     convex_hull = mcp.plot_mcp(confidence_level)

#     # Now convex_hull contains the coordinates of the Minimum Convex Polygon for the specified confidence level
#     print("Coordinates of Minimum Convex Polygon for the specified confidence level:")
#     # for point in convex_hull:
#     #     print(point)
#     print(len(convex_hull))
import os

script_path = 'E:\\HomeZ_Deploy\\HomeZ-main\\tests\\frontend.py'
print(os.path.exists(script_path))
