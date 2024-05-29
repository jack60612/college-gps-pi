"""This file converts it from extracted OSM data to the osmnx format"""

source_path = "north-america-all-roads.osm.pbf"

import osmnx as ox
from networkx import MultiDiGraph
from pyrosm import OSM


def get_graph(file_name: str) -> MultiDiGraph:
    osm = OSM(file_name)
    print("Getting driving network")
    nodes, edges = osm.get_network(network_type="driving")
    print("Converting to graphml")
    graph = osm.to_graph(nodes, edges, network_type="networkx")
    
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
