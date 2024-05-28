"""This file converts it from extracted OSM data to the osmnx format"""

source_path = "north-america-all-roads.osm.pbf"

import osmnx as ox
from networkx import MultiDiGraph
from pyrosm import OSM


def get_graph(file_name: str) -> MultiDiGraph:
    osm = OSM(file_name)
    print("Getting driving network")
    driving_net = osm.get_network(network_type="driving")
    return driving_net


def main() -> None:
    # we only need the path finding
    main_graph = get_graph(source_path)
    print("Graph loaded\nSaving Graph...")
    ox.save_graphml(main_graph, "north-america-all-roads.graphml")
    print("Graph saved, exiting...")


if __name__ == "__main__":
    main()
