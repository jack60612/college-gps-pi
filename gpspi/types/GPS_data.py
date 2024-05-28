import datetime
from dataclasses import dataclass, field
from typing import Optional

from gpspi.types.saved_data import Waypoint


@dataclass
class GPSData:
    """Class to store GPS data. All fields are optional, as the GPS may not have a fix at all times."""

    latitude: Optional[float] = field(default=None)  # the latitude in degrees
    longitude: Optional[float] = field(default=None)  # the longitude in degrees
    altitude: Optional[float] = field(default=None)  # altitude in meters
    speed: Optional[float] = field(default=None)  # m/s
    satellites: list[dict[str, object]] = field(default_factory=list)  # Number of satellites
    time: Optional[datetime.datetime] = field(default=None)  # UTC time
    true_heading: Optional[float] = field(default=None)  # heading in degrees (true north)
    mag_heading: Optional[float] = field(default=None)  # heading in degrees (magnetic)

    @property
    def in_sync(self) -> bool:
        "If the gps data is less then 5 seconds old, return True, else False"
        if self.time is None:
            return False
        return ((self.time - datetime.datetime.now(datetime.UTC)).total_seconds() < 5) and self.latitude is not None

    @property
    def num_satellites(self) -> int:
        return len(self.satellites)

    def as_waypoint(self) -> Waypoint:
        assert (
            self.latitude is not None
            and self.longitude is not None
            and self.altitude is not None
            and self.time is not None
        )
        return Waypoint(self.latitude, self.longitude, self.altitude, name=f"WP {self.time.isoformat()}")

    def update_position_data(
        self,
        latitude: Optional[float],
        longitude: Optional[float],
        altitude: Optional[float],
        speed: Optional[float],
        time: Optional[str],
        true_heading: Optional[float],
        mag_heading: Optional[float],
    ) -> None:
        self.latitude = latitude if latitude is not None else self.latitude
        self.longitude = longitude if longitude is not None else self.longitude
        self.altitude = altitude if altitude is not None else self.altitude
        self.speed = speed if speed is not None else self.speed
        self.time = datetime.datetime.fromisoformat(time) if time is not None else self.time
        self.true_heading = true_heading if true_heading is not None else self.true_heading
        self.mag_heading = mag_heading if mag_heading is not None else self.mag_heading

    def update_satellite_data(self, time: Optional[str], satellites: list[dict[str, object]]) -> None:
        self.time = datetime.datetime.fromisoformat(time) if time is not None else self.time
        self.satellites = satellites if satellites is not None else self.satellites


@dataclass(frozen=True)
class CityData:
    """Class to store city data"""

    name: str  # the name of the city
    country_code: str  # the country code of the city
    latitude: float  # the latitude of the city
    longitude: float  # the longitude of the city
    admin1: str  # the state or province of the city
    admin2: str  # the county of the city

    def get_full_name(self) -> str:
        return f"{self.name}, {self.admin2}, {self.admin1}, {self.country_code}"

    def as_waypoint(self) -> Waypoint:
        return Waypoint(self.latitude, self.longitude, 0, name=self.get_full_name())
