"""This file converts it from extracted OSM data to the osmnx format"""

#source_path = "north-america-all-roads.osm.pbf"
source_path = "florida-all-roads.osm.pbf"

import datetime
import osmnx as ox
from networkx import MultiDiGraph
from pyrosm import OSM


def miles_to_degrees(miles):
    """Convert miles to degrees (approximately)."""
    return miles / 69.0

def get_bounding_box(lat, lon, radius_miles=50) -> tuple[float,float,float,float]:
    """
    Returns a bounding box representing a circle of a given radius (in miles) around a coordinate point.

    Parameters:
    - lat (float): Latitude of the center point.
    - lon (float): Longitude of the center point.
    - radius_miles (float): Radius of the circle in miles. Default is 50 miles.

    Returns:
    - tuple: A tuple containing the min lat and min long then max lat and max long
    """
    radius_degrees = miles_to_degrees(radius_miles)
    min_lat = lat - radius_degrees
    max_lat = lat + radius_degrees
    min_lon = lon - radius_degrees
    max_lon = lon + radius_degrees
    
    return (min_lon, min_lat, max_lon, max_lat)


def get_graph(file_name: str) -> MultiDiGraph:
    
    b_box = list(get_bounding_box(27.994402, -81.760254, 50))
    
    
    #osm = OSM(file_name, b_box)
    osm = OSM(file_name)
    print("Getting driving network")
    time = datetime.datetime.now()
    nodes, edges = osm.get_network(nodes=True,network_type="driving")
    print(f"Time taken: {datetime.datetime.now() - time}")
    print("Converting to graphml")
    time = datetime.datetime.now()
    graph = osm.to_graph(nodes, edges, graph_type="networkx")
    print(f"Time taken: {datetime.datetime.now() - time}")
    
    return graph


def main() -> None:
    # we only need the path finding
    main_graph = get_graph(source_path)
    print("graph loaded, simplifying...")
    ox.simplify_graph(main_graph)
    print("graph simplified, saving graph to disk")
    ox.save_graphml(main_graph, "north-america-all-roads.graphml")
    print("Graph saved, exiting...")


if __name__ == "__main__":
    main()
