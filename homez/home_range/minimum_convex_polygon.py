"""
Copyrigth 2024 HomeZ

Minimum Convex Polygon
----------------------
"""

# Author: Sicoprogrammer <pranavrimc@gmail.com>
# Modified: [Adam-Al-Rahman]

from shapely.geometry import Point, MultiPoint
import matplotlib.pyplot as plt


class MinimumConvexPolygon:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def mcp(self):
    # Converting into shapley points
    points = [Point(xy) for xy in zip(self.x, self.y)]

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

    return mcp_results

  def plot(self, output_raster_path: str):
    mcp_results = self.mcp()

    # Plotting MCP
    _, ax = plt.subplots(figsize=(10, 10))
    for percent, mcp in mcp_results:
      if mcp.geom_type == 'Polygon':
        x, y = mcp.exterior.xy
        ax.fill(x, y, alpha=0.5, label=f"{percent}% of points")

    ax.scatter(self.x, self.y, color='black', s=5, label='Points')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('MCP for Different Percentages of Points')
    plt.legend()
    plt.savefig(output_raster_path, format='tif')

  def create_raster(self, output_raster_path):
    pass
