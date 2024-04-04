import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
amphi = pd.read_csv("D:/Coding/HomeZ/homez/home_range/minimum_convex_polygon/tracking_sample.csv")


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

plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('MCP for Different Percentages of Points')
plt.legend()
plt.show()
