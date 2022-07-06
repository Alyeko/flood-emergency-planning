from rtree import index
from shapely.geometry import Point


class NearestNode:
    def __init__(self, itn_data, coordinate, peak):
        self.itn = itn_data
        self.coordinate = coordinate.values[0]
        self.peak = peak.values[0]

    def create_idx(self):
        """Takes itn data passed, creates an rtree index and returns both itn and rtree index"""
        idx = index.Index()
        for i in enumerate(self.itn['roadnodes']):
            idx.insert(i[0], self.itn['roadnodes'][i[1]]['coords'], {'obj': i})
        return self.itn, idx

    def nearest_itn_node(self):
        """1. Uses itn data read, rtree created and coordinates passed to find the nearest node to those coordinates ie that of the user and highest peak.
           2. Returns nearest itn nodes to user and peak(eg=osgb4000000026142827) and Shapely Points of the coordinates."""

        itn, idx = self.create_idx()
        nearest_node_to_user = list(idx.nearest((self.coordinate.bounds), 1, objects=True))[0].object['obj'][1]
        nearest_node_to_peak = list(idx.nearest((self.peak.bounds), 1, objects=True))[0].object['obj'][1]
        user_node_coord = Point(tuple(itn['roadnodes'][nearest_node_to_user]['coords'][0:2]))
        peak_node_coord = Point(tuple(itn['roadnodes'][nearest_node_to_peak]['coords'][0:2]))
        return nearest_node_to_user, nearest_node_to_peak, user_node_coord, peak_node_coord
