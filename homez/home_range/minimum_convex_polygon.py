"""
Copyrigth 2024 HomeZ

Minimum Convex Polygon
----------------------
"""

# Author: Sicoprogrammer <pranavrimc@gmail.com>
# Modified: [Adam-Al-Rahman]

import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
turtle = pd.read_csv("D:/Coding/HomeZ/homez/home_range/tracking_sample.csv")

# Drop rows with missing coordinates
turtle.dropna(subset=['x', 'y'], inplace=True)

# Extract x and y coordinates
x_coords = turtle['x'].tolist()
y_coords = turtle['y'].tolist()

# MCP algorithm
def mcp_algorithm(x_coords, y_coords):
    points = list(zip(x_coords, y_coords))
    points.sort()  # Sort points by x-coordinate

    upper_hull = []
    lower_hull = []

    # Compute upper hull
    for p in points:
        while len(upper_hull) >= 2 and cross_product(upper_hull[-2], upper_hull[-1], p) <= 0:
            upper_hull.pop()
        upper_hull.append(p)

    # Compute lower hull
    for p in reversed(points):
        while len(lower_hull) >= 2 and cross_product(lower_hull[-2], lower_hull[-1], p) <= 0:
            lower_hull.pop()
        lower_hull.append(p)

    # Combine upper and lower hulls to form the convex hull
    convex_hull = upper_hull[:-1] + lower_hull[:-1]
    return convex_hull

def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

# Calculate the convex hull for different percentages
mcp_results = []
percentages = range(50, 105, 5)
for percent in percentages:
    num_points = int(len(x_coords) * percent / 100)
    if num_points < 3:
        continue
    convex_hull = mcp_algorithm(x_coords[:num_points], y_coords[:num_points])
    mcp_results.append((percent, convex_hull))

# Plotting MCP
fig, ax = plt.subplots(figsize=(10, 10))
for percent, convex_hull in mcp_results:
    x, y = zip(*convex_hull)
    ax.fill(x, y, alpha=0.5, label=f"{percent}% of points")

ax.scatter(x_coords, y_coords, color='black', s=5, label='Points')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('MCP for Different Percentages of Points')
plt.legend()
plt.show()


plt.savefig(output_raster_path, format='tif')

def create_raster(self, output_raster_path):
    pass
