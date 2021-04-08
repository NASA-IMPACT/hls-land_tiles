import cartopy.crs as ccrs
import geopandas
import matplotlib.pyplot as plt

s2tiles = geopandas.read_file("s2_grid.json")

with open("HLS.land.tiles.txt","r") as f:
    hls_tilelist = [x.strip("\n") for x in f.readlines()]
hlstiles = s2tiles[s2tiles['identifier'].isin(hls_tilelist)]

fig = plt.figure(figsize=[10,6],dpi=300,facecolor=None)
ax = fig.add_axes([0.01,0.01,0.98,0.98],projection = ccrs.Robinson())
ax.add_geometries(hlstiles.geometry, crs=ccrs.PlateCarree(), facecolor='green', edgecolor='green', zorder=5)

ax.set_global()
ax.coastlines()
ax.stock_img()
plt.savefig("HLS.land.tiles.png",transparent=True)
