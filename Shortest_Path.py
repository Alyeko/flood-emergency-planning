import networkx as ntx
import geopandas as gpd
from shapely.geometry import *
import numpy as np


# parent_dir = 'Your parent directory'
def shortestpath(elevation, itn, nearest_node_to_user, nearest_node_to_peak):
    ele = elevation.read(1)   # Store raster data as an array
    road_links = itn['roadlinks']
    path_graph = ntx.Graph()  # The graph is used to save the time weight of each edge

    ############################################################################
    # This loop is used to create a graph that stores the weight of each road_link.
    # The main purpose is to calculate the weight of each road by
    # calculating the height difference between every two nodes.
    for link in road_links:
        link_id = link
        link_length = road_links[link]['length']
        ####################################
        # Step1. Initialize the weight to not consider the time spent on uphill
        weight = link_length / (5000 / 60)  # Unitize it to minutes

        ####################################
        # Step2. Extract all nodes contained in this road_link
        node_x = []
        node_y = []
        for i in road_links[link]['coords']:
            node_x.append(i[0])
            node_y.append(i[1])
        row_0, col_0 = elevation.index(node_x[0], node_y[0])
        #  Index the row and column of the out point in the raster_array

        ####################################
        # step3. Calculate the height difference between every two nodes
        # to determine whether it is necessary to increase the weight of this road_link
        elevation1 = ele[row_0][col_0]  # The height of the first node
        for i in range(1, len(node_x)):
            row, col = elevation.index(node_x[i], node_y[i])
            elevation2 = ele[row][col]  # The height of the second node
            delta = elevation2 - elevation1  # Calculate the height difference between two nodes
            if delta > 0:  # When the difference is positive, it means that every 10 meters walk plus 1 minute
                weight = weight + delta / 10
            elevation1 = elevation2

        #####################################
        # step4. Add each road_link and it's weight to the graph
        path_graph.add_edge(road_links[link]['start'], road_links[link]['end'], length=link_length, link_id=link_id,
                            weight=weight)
    ############################################################################

    # Use the weighted shortest path function in networkx to find the shortest path
    shortest_road = ntx.dijkstra_path(path_graph, source=nearest_node_to_user, target=nearest_node_to_peak,
                                      weight='weight')

    '''Here is extra code to manipulate the output of algorithm to georeferenced point for the sack of plotting'''
    links = []  # this list will be used to populate the feature id (fid) column
    geom = []  # this list will be used to populate the geometry column

    time = 0
    first_node = shortest_road[0]
    for node in shortest_road[1:]:
        link_fid = path_graph.edges[first_node, node]['link_id']  # if fid doesnt work, change value to link_id
        links.append(link_fid)
        time = time + path_graph.edges[first_node, node]['weight']
        geom.append(LineString(road_links[link_fid]['coords']))
        first_node = node

    path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})
    print("The shortest path cost about " + str(np.round(time, 0)) +
          " minutes for you to reach the closest highest peak!")

    return path_gpd

# with open(os.path.join(parent_dir, 'itn', 'solent_itn.json'), 'r') as f:
#     path = json.load(f)
# road_nodes = path['roadnodes']
# j = 0
# user_node = ''
# peak_node = ''
# for i in road_nodes:
#     if j == 200:
#         user_node = i
#     if j == 300:
#         peak_node = i
#         break
#     j = j + 1
# print(user_node)
# print(peak_node)
# sp = shortestpath(user_node, peak_node)
# print(sp)
