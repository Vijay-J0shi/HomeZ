"""
Copyrigth 2024 HomeZ

Minimum Convex Polygon
----------------------
"""

# Author: Sicoprogrammer <pranavrimc@gmail.com>
# Modified: [Adam-Al-Rahman]

import matplotlib.pyplot as plt


class MinimumConvexPolygon:

  def __init__(self, x, y):
    self.x = x.tolist()
    self.y = y.tolist()

  def cross_product(self, o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

  # MCP algorithm
  def mcp_algorithm(self):
    points = list(zip(self.x, self.y))
    points.sort()  # Sort points by x-coordinate

    upper_hull = []
    lower_hull = []

    # Compute upper hull
    for p in points:
      while len(upper_hull) >= 2 and self.cross_product(upper_hull[-2], upper_hull[-1], p) <= 0:
        upper_hull.pop()
      upper_hull.append(p)

    # Compute lower hull
    for p in reversed(points):
      while len(lower_hull) >= 2 and self.cross_product(lower_hull[-2], lower_hull[-1], p) <= 0:
        lower_hull.pop()
      lower_hull.append(p)

    # Combine upper and lower hulls to form the convex hull
    convex_hull = upper_hull[:-1] + lower_hull[:-1]
    return convex_hull

  def convex_hull(self):
    # Calculate the convex hull for different percentages
    mcp_results = []
    percentages = range(50, 105, 5)
    for percent in percentages:
      num_points = int(len(self.x) * percent / 100)
      if num_points < 3:  # minimum point required for polygon
        continue
      convex_hull = self.mcp_algorithm(self.x[:num_points], self.y[:num_points])
      mcp_results.append((percent, convex_hull))

    return mcp_results

  def plot(self, output_raster_path, alpha=0.5):
    # Plotting MCP
    mcp_results = self.convex_hull()
    _, ax = plt.subplots(figsize=(10, 10))
    for percent, convex_hull in mcp_results:
      x, y = zip(*convex_hull)
      ax.fill(x, y, alpha=alpha, label=f"{percent}% of points")

    ax.scatter(self.x, self.y, color='black', s=5, label='Points')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('MCP for Different Percentages of Points')
    plt.legend()
    plt.savefig(output_raster_path, format='tif')
