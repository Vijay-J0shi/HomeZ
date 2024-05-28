import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from scipy.stats import gaussian_kde

# Create some random points with latitude and longitude
num_points = 100
latitude = np.random.uniform(low=-90, high=90, size=num_points)
longitude = np.random.uniform(low=-180, high=180, size=num_points)

# Create a GeoDataFrame from the points
geometry = [Point(lon, lat) for lon, lat in zip(longitude, latitude)]
gdf = gpd.GeoDataFrame(geometry=geometry, crs='EPSG:4326')

# Extract latitude and longitude coordinates
latitude = gdf.geometry.y
longitude = gdf.geometry.x

# Perform KDE
xy = np.vstack([longitude, latitude])
kde = gaussian_kde(xy, bw_method=0.5)  # bw_method is the bandwidth parameter

# Create grid to evaluate kde
lat_min, lat_max = latitude.min() - 1, latitude.max() + 1
lon_min, lon_max = longitude.min() - 1, longitude.max() + 1
X, Y = np.mgrid[lon_min:lon_max:100j, lat_min:lat_max:100j]
positions = np.vstack([X.ravel(), Y.ravel()])
Z = np.reshape(kde(positions).T, X.shape)

# Plot the results
fig, ax = plt.subplots()
ax.imshow(np.rot90(Z), cmap=plt.cm.viridis, extent=[lon_min, lon_max, lat_min, lat_max])
ax.plot(longitude, latitude, 'k.', markersize=2)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Kernel Density Estimation (KDE) of Random Points')
plt.show()
