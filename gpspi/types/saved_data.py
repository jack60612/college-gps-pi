from dataclasses import dataclass, field
from typing import Optional, TypedDict


class DictWaypoint(TypedDict):
    latitude: float
    longitude: float
    altitude: float


class DictSavedData(TypedDict):
    destination: Optional[DictWaypoint]
    waypoints: list[DictWaypoint]


@dataclass(frozen=True)
class Waypoint:
    latitude: float
    longitude: float
    altitude: float

    @classmethod
    def from_dict(cls, data: DictWaypoint) -> "Waypoint":
        return cls(data["latitude"], data["longitude"], data["altitude"])

    def to_dict(self) -> "DictWaypoint":
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
        }


@dataclass
class SavedData:
    destination: Optional[Waypoint] = None
    waypoints: list[Waypoint] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: DictSavedData) -> "SavedData":
        return cls(
            Waypoint.from_dict(data["destination"]) if data["destination"] else None,
            [Waypoint.from_dict(waypoint) for waypoint in data["waypoints"]],
        )

    def to_dict(self) -> "DictSavedData":
        return {
            "destination": self.destination.to_dict() if self.destination else None,
            "waypoints": [waypoint.to_dict() for waypoint in self.waypoints],
        }
