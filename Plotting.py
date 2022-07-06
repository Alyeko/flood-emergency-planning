import matplotlib.pyplot as plt
import numpy as np
from rasterio.plot import show
from cartopy import crs
from matplotlib_scalebar.scalebar import ScaleBar
from HighestPoint import HIGHEST_PEAK


def plotting(elevation, buf, background, path_gpd, coordinate):
    back_array = background.read(1)
    palette = np.array([value for key, value in background.colormap(1).items()])
    background_image = palette[back_array]
    bounds = background.bounds
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
    display_extent = [coordinate[0].x - 7000, coordinate[0].x + 7000,
                      coordinate[0].y - 5000, coordinate[0].y + 5000]

    masks, mask_transform = HIGHEST_PEAK(elevation, buf).buffer_mask()
    highest_peak = HIGHEST_PEAK(elevation, buf).high_coord()

    fig = plt.figure(figsize=(12, 10), dpi=300)
    ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())
    ax.imshow(background_image, extent=extent, zorder=0)
    out_mask = np.ma.masked_where(masks == 0, masks)
    show(out_mask, cmap='terrain', transform=mask_transform, alpha=0.4, ax=ax)
    path_gpd.plot(ax=ax, edgecolor='red', linewidth=3, label="Shortest Path", zorder=2)
    coordinate.plot(ax=ax, marker="X", color="yellow", label="User's Location", zorder=3)
    highest_peak.plot(ax=ax, marker="X", color="green", label="Highest Peak", zorder=4)
    ax.set_extent(display_extent, crs=crs.OSGB())
    leg = ax.legend(title="Legend")
    leg.set_bbox_to_anchor((0., 0., 0.2, 0.2))
    ax.add_artist(ScaleBar(1, location='lower right', box_alpha=0))
    plt.show()
