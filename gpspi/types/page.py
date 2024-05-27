from enum import Enum


class Page(Enum):
    TIME_AND_SATELLITES: int = 1
    GPS_COORDINATES: int = 2
    SELECT_DESTINATION: int = 3
    SELECT_WAYPOINTS: int = 4
    COMPASS_HEADING_AND_SPEED: int = 5
