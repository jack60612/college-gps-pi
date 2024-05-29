from dataclasses import Field, dataclass
from typing import Optional

import osmnx as ox
from networkx import MultiDiGraph
from osmnx import distance

from gpspi.types.GPS_data import GPSData
from gpspi.types.saved_data import Waypoint


@dataclass
class GPSPathFinder:
    graph_path: str
    nav_graph: MultiDiGraph = Field(default=None, init=False)  # gets set in __post_init__

    def __post_init__(self) -> None:
        self.nav_graph: MultiDiGraph = ox.load_graphml(self.graph_path)

    def find_nearest_node(self, target_waypoint: Waypoint) -> int:
        node_ids: list[int] = distance.nearest_nodes(
            self.nav_graph, target_waypoint.latitude, target_waypoint.longitude
        )
        return node_ids[0]

    def find_node_by_id(self, node_id: int, name: Optional[str] = None) -> Waypoint:
        node = self.nav_graph.nodes[node_id]
        return Waypoint(node["y"], node["x"], 0.0, name=name if name else node["name"])

    def find_nearest_road(self, current_position: GPSData) -> int:
        current_pos_waypoint = current_position.as_waypoint()
        road_node_id = self.find_nearest_node(current_pos_waypoint)
        return road_node_id

    def navigate_to_nearest_road(self, current_position: GPSData) -> Waypoint:
        nearest_node = self.find_nearest_road(current_position)
        nearest_node_coords = self.find_node_by_id(nearest_node, name="Nearest Rd")
        return nearest_node_coords

    def navigate_to_waypoint(self, current_position: GPSData, target_waypoint: Waypoint) -> list[Waypoint]:
        output_points: list[Waypoint] = []
        # get nearest road (node id)
        nearest_node = self.find_nearest_road(current_position)

        # destination waypoint (node id)
        destination_node = self.find_nearest_node(target_waypoint)

        # get all node ids between the two nodes
        shortest_path = ox.shortest_path(self.nav_graph, nearest_node, destination_node)
        for node in shortest_path:
            node_coords = self.find_node_by_id(node)
            output_points.append(node_coords)

        return output_points
