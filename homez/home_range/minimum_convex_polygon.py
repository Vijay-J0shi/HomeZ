class MinimumConvexPolygon:
    def __init__(self, points, alpha):
        self.points = points
        self.alpha = alpha

    def mcp_algorithm(self):
        points = sorted(self.points)

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

    def cross_product(self, o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def plot_mcp(self):
        convex_hull = self.mcp_algorithm()

        # Plotting MCP
        fig, ax = plt.subplots(figsize=(10, 10))
        x, y = zip(*convex_hull)
        ax.fill(x, y, alpha=self.alpha)
        ax.scatter(*zip(*self.points), color='black', s=5, label='Points')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Minimum Convex Polygon')
        plt.legend()

        # Save plot as tif image
        buffer = BytesIO()
        plt.savefig(buffer, format='tiff')
        buffer.seek(0)


        return buffer

    def calculate_area(self):
        convex_hull = self.mcp_algorithm()
        n = len(convex_hull)
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += convex_hull[i][0] * convex_hull[j][1]
            area -= convex_hull[j][0] * convex_hull[i][1]
        area = abs(area) / 2.0
        return area

    def get_corner_points(self):
        return self.mcp_algorithm()


turtle = pd.read_csv("/content/tracking_sample.csv")
turtle.dropna(subset=['x', 'y'], inplace=True)
points = [(float(x), float(y)) for x, y in zip(turtle['x'], turtle['y'])]

mcp = MinimumConvexPolygon(points, alpha=0.5)
image_buffer = mcp.plot_mcp()
area = mcp.calculate_area()
print("Area of the Minimum Convex Polygon:", area)
corner_points = mcp.get_corner_points()
print("Corner Points:", corner_points)


with open('mcp_plot.tiff', 'wb') as f:
    f.write(image_buffer.getvalue())
