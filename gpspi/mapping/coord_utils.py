from typing import Union

import reverse_geocoder as rg
from osmnx import bearing, distance

from gpspi.types.GPS_data import CityData
from gpspi.types.saved_data import Waypoint


def get_magnetic_bearing(current_pos: Waypoint, target_pos: Waypoint) -> float:
    """
    Returns the bearing from the current position to the target position
    :param current_pos: the current position
    :param target_pos: the target position
    :return: the bearing (degeees) from the current position to the target position
    """
    # lat 1 and lon 1 are the current position
    lat1 = current_pos.latitude
    lon1 = current_pos.longitude
    # lat 2 and lon 2 are the target position
    lat2 = target_pos.latitude
    lon2 = target_pos.longitude
    # return the bearing
    true_bearing = bearing.calculate_bearing(lat1, lon1, lat2, lon2)
    offset = 0  # TODO: get the magnetic offset
    magnetic_bearing = true_bearing + offset
    return magnetic_bearing


def get_distance_meters(current_pos: Waypoint, target_pos: Waypoint) -> float:
    """
    Returns the distance from the current position to the target position
    :param current_pos: the current position
    :param target_pos: the target position
    :return: the distance (meters) from the current position to the target position
    """
    # lat 1 and lon 1 are the current position
    lat1 = current_pos.latitude
    lon1 = current_pos.longitude
    # lat 2 and lon 2 are the target position
    lat2 = target_pos.latitude
    lon2 = target_pos.longitude
    # use the haversine formula to calculate the distance
    dist_meters = distance.great_circle(lat1, lon1, lat2, lon2)
    return dist_meters


def get_distance_feet(current_pos: Waypoint, target_pos: Waypoint) -> float:
    """
    Returns the distance from the current position to the target position
    :param current_pos: the current position
    :param target_pos: the target position
    :return: the distance (feet) from the current position to the target position
    """
    dist_meters = get_distance_meters(current_pos, target_pos)
    dist_feet = dist_meters * 3.28084
    return dist_feet


def get_nearest_city(current_pos: Waypoint) -> CityData:
    """
    Returns the nearest city to the current position
    :param current_pos: the current position
    :return: the nearest city to the current position
    """
    lat = current_pos.latitude
    lon = current_pos.longitude
    # get the nearest city
    results: list[dict[str, Union[str, float]]] = rg.search((lat, lon))
    if len(results) == 0:
        return CityData("", "", 0, 0, "", "")
    city = results[0]
    name: str = str(city["name"])
    r_lat: float = float(city["lat"])
    r_lon: float = float(city["lon"])
    cc: str = str(city["cc"])
    admin1: str = str(city["admin1"])
    admin2: str = str(city["admin2"])
    return CityData(name, cc, r_lat, r_lon, admin1, admin2)
