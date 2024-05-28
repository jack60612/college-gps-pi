from dataclasses import Field, dataclass

import osmnx as ox
from networkx import MultiDiGraph


@dataclass
class GPSPathFinder:
    graph_path: str
    nav_graph: MultiDiGraph = Field(default=None, init=False)  # gets set in __post_init__

    def __post_init__(self) -> None:
        self.nav_graph: MultiDiGraph = ox.load_graphml(self.graph_path)
