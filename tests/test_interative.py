import numpy as np
import geopandas as gpd
import folium
from shapely.geometry import Point
from scipy.stats import gaussian_kde

# Generate synthetic data for demonstration
np.random.seed(0)
n_samples = 1000
# Set latitudes and longitudes near Mumbai, India
lon = np.random.uniform(low=72, high=73, size=n_samples)  # Longitudes near Mumbai
lat = np.random.uniform(low=18.9, high=19.2, size=n_samples)  # Latitudes near Mumbai

# Create GeoDataFrame with synthetic points
geometry = [Point(xy) for xy in zip(lon, lat)]
gdf = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")

# Perform KDE using scipy's gaussian_kde
coords = np.vstack([lon, lat])
# Adjust bandwidth to increase density near Mumbai
kde = gaussian_kde(coords, bw_method=0.05)  # Decreased bandwidth for higher density near Mumbai

# Create grid for plotting KDE on Earth's surface
lon_min, lon_max = lon.min(), lon.max()
lat_min, lat_max = lat.min(), lat.max()
lons = np.linspace(lon_min, lon_max, 300)  # Increased points for finer resolution
lats = np.linspace(lat_min, lat_max, 200)  # Increased points for finer resolution
grid_lons, grid_lats = np.meshgrid(lons, lats)
grid_coords = np.vstack([grid_lons.ravel(), grid_lats.ravel()])

# Evaluate KDE on the grid
density = kde(grid_coords)

# Create an interactive map using folium
map_center = [(lat_min + lat_max) / 2, (lon_min + lon_max) / 2]
mymap = folium.Map(location=map_center, zoom_start=10)  # Increased initial zoom level

# Convert grid to map coordinates
x, y = np.meshgrid(lons, lats)
heatmap = folium.raster_layers.ImageOverlay(
  image=density.reshape(x.shape),
  bounds=[[lat_min, lon_min], [lat_max, lon_max]],
).add_to(mymap)

# Create custom colormap
colors = ['#000000', '#330066', '#660099', '#9900CC', '#CC00FF', '#FF33FF', '#FF66FF', '#FF99FF', '#FFCCFF', '#FFFFFF']
colormap = folium.LinearColormap(colors=colors,
                                 index=[density.min(), density.max()],
                                 vmin=density.min(),
                                 vmax=density.max())

# Add colorbar legend to the map
colormap.caption = 'Density'
mymap.add_child(colormap)

# Save the map as an HTML file with specified initial center and zoom level
mymap.save("interactive_kde_map_mumbai.html")
