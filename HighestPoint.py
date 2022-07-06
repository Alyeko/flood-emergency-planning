import rasterio
from rasterio.mask import mask
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
from pyproj import CRS


class HIGHEST_PEAK:
    crs = CRS.from_epsg(27700)

    def __init__(self, elevation_file, buffer_geom, crs=crs):
        self.buf = buffer_geom
        self.elevation = elevation_file
        self.crs = crs

    # Buffer Mask (Raster Clipping)
    def buffer_mask(self):
        masks, mask_transform = mask(dataset=self.elevation, shapes=self.buf.geometry, crop=True, indexes=1)
        return masks, mask_transform

    def high_coord(self):
        masks, mask_transform = self.buffer_mask()
        # Highest Peak Identification
        indices = np.where(masks == masks.max())
        # Only take the first highest point if there are multiples, ignore the index (index = indices[0])
        xmax = indices[0][0]
        ymax = indices[1][0]
        # Georeference the Highest Peak
        highest_peak = gpd.GeoSeries(Point(rasterio.transform.xy(mask_transform, xmax, ymax)), crs=self.crs)
        return highest_peak
