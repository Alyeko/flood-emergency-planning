"""Main file which solves the Flood Emergency Planning Task"""
from utilities import user_coords
from HighestPoint import HIGHEST_PEAK
from get_nearest_node import NearestNode
from Shortest_Path import shortestpath
from Plotting import plotting
import os, rasterio, json


def main():
    # Task 1
    # read input
    # Reading Files
    parent_dir = "Your Parent Dir"
    background = rasterio.open(os.path.join(parent_dir, 'background', 'raster-50k_2724246.tif'))
    elevation = rasterio.open(os.path.join(parent_dir, 'elevation', 'SZ.asc'))
    with open(os.path.join(parent_dir, 'itn', 'solent_itn.json'), 'r') as f:
        itn_data = json.load(f)
    coord_ref = elevation.crs

    coordinate = user_coords(elevation)
    buffer = coordinate.buffer(5000)

    # Task 2
    # User input locations to generate georeference coordinates and 5 kilometer buffer
    highest_peak = HIGHEST_PEAK(elevation, buffer, coord_ref).high_coord()

    # Task 3
    # Creation of rtree for itn nodes
    get = NearestNode(itn_data, coordinate, highest_peak)
    get.create_idx()
    nearest_node_to_user = get.nearest_itn_node()[0]
    nearest_node_to_peak = get.nearest_itn_node()[1]

    # Task 4
    # Shortest path
    path_gpd = shortestpath(elevation, itn_data, nearest_node_to_user, nearest_node_to_peak)

    # Task 5
    # Plotting
    plotting(elevation, buffer, background, path_gpd, coordinate)


if __name__ == '__main__':
    main()
    print('all done!')
