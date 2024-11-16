from enum import Enum


class Page(Enum):
    TIME_AND_SATELLITES: int = 0
    GPS_COORDINATES: int = 1
    SELECT_DESTINATION: int = 2
    SELECT_WAYPOINTS: int = 3
    COMPASS_HEADING_AND_SPEED: int = 4
    COORDINATES_AND_DISTANCE: int = 5
    MIT_PAGE: int = 6
