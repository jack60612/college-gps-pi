from dataclasses import dataclass, field
import datetime
from typing import Any, Optional


@dataclass
class GPSData:
    """Class to store GPS data. All fields are optional, as the GPS may not have a fix at all times."""

    latitude: Optional[float] = field(default=None)  # the latitude in degrees
    longitude: Optional[float] = field(default=None)  # the longitude in degrees
    altitude: Optional[float] = field(default=None)  # altitude in meters
    speed: Optional[float] = field(default=None)  # m/s
    satellites: list[dict[str, object]] = field(default=list())  # Number of satellites
    time: Optional[datetime.datetime] = field(default=None)  # UTC time
    true_heading: Optional[float] = field(
        default=None
    )  # heading in degrees (true north)
    mag_heading: Optional[float] = field(default=None)  # heading in degrees (magnetic)

    @property
    def in_sync(self) -> bool:
        "If the gps data is less then 5 seconds old, return True, else False"
        if self.time is None:
            return False
        return (
            (self.time - datetime.datetime.now(datetime.UTC)).total_seconds() < 5
        ) and self.latitude is not None

    @property
    def num_satellites(self) -> int:
        return len(self.satellites)

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
        self.latitude = latitude if latitude else self.latitude
        self.longitude = longitude if longitude else self.longitude
        self.altitude = altitude if altitude else self.altitude
        self.speed = speed if speed else self.speed
        self.time = datetime.datetime.fromisoformat(time) if time else self.time
        self.true_heading = true_heading if true_heading else self.true_heading
        self.mag_heading = mag_heading if mag_heading else self.mag_heading

    def update_satellite_data(
        self, time: Optional[str], satellites: list[dict[str, object]]
    ) -> None:
        self.time = datetime.datetime.fromisoformat(time) if time else self.time
        self.satellites = satellites if satellites else self.satellites
