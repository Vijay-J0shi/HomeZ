"""
Copyrigth 2024 HomeZ
"""
import pandas as pd
from shapely.geometry import Point, MultiPoint
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt

amphi = pd.read_csv("D:/Coding/HomeZ/homez/home_range/minimum_convex_polygon/tracking_sample.csv")

amphi.dropna(subset=['x', 'y'], inplace=True)

points = [Point(xy) for xy in zip(amphi['x'], amphi['y'])]  # Converting into shapley points

# Calculating convex hull for different percentages
mcp_results = []
percentages = range(50, 105, 5)
for percent in percentages:
  num_points = int(len(points) * percent / 100)
  if num_points < 3:
    continue
  mcp = MultiPoint(points[:num_points]).convex_hull
  if not mcp.is_empty:
    mcp_results.append((percent, mcp))

# Plotting MCP
fig, ax = plt.subplots(figsize=(10, 10))
for percent, mcp in mcp_results:
  if mcp.geom_type == 'Polygon':
    x, y = mcp.exterior.xy
    ax.fill(x, y, alpha=0.5, label=f"{percent}% of points")
ax.scatter(amphi['x'], amphi['y'], color='black', s=5, label='Points')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('MCP for Different Percentages of Points')
plt.legend()
plt.show()
