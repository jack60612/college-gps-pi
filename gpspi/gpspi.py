import logging
from typing import Optional
from gpspi.button_handler import ButtonHandler, LCDButton
from gpspi.types.saved_data import DictSavedData, SavedData, Waypoint
from gpspi.LCD_handler import LCDHandler
import gps
import time
import json
from enum import Enum

# GPIO Pins
KEY_UP_PIN: int = 6
KEY_DOWN_PIN: int = 19
KEY_LEFT_PIN: int = 5
KEY_RIGHT_PIN: int = 26
KEY_PRESS_PIN: int = 13
KEY1_PIN: int = 21
KEY2_PIN: int = 20
KEY3_PIN: int = 16


class Page(Enum):
    TIME_AND_SATELLITES: int = 0
    GPS_COORDINATES: int = 1
    SELECT_DESTINATION: int = 2
    SELECT_WAYPOINTS: int = 3
    COMPASS_HEADING_AND_SPEED: int = 4


class GPSDisplay:
    def __init__(self, lcd_handler: LCDHandler, gpio_handler: ButtonHandler) -> None:
        self.lcd_handler: LCDHandler = lcd_handler
        self.gpio_handler: ButtonHandler = gpio_handler

        # GPS setup
        logging.info("Connecting to GPSD")
        self.session = gps.gps(host="127.0.0.1", port="2947", reconnect=True)
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        logging.info("Connected to GPSD")

        # Screen variables
        self.current_screen: Page = Page.TIME_AND_SATELLITES
        self.total_screens: int = 4
        self.saved_data: SavedData = self.load_data()
        self.cur_waypoint_index: int = 0

        # Configure button callbacks
        self.gpio_handler.configure_callbacks(self.button_callback)
        logging.info("Button callbacks configured")

    def load_data(self) -> SavedData:
        try:
            with open("destination.json", "r") as f:
                return SavedData(DictSavedData(**json.load(f)))  # type: ignore
        except FileNotFoundError:
            return SavedData()

    def save_data(self) -> None:
        with open("destination.json", "w") as f:
            json.dump(self.saved_data.to_dict(), f)

    def button_callback(self, button: LCDButton) -> None:
        if button == LCDButton.UP:
            self.current_screen = Page(
                (self.current_screen.value - 1) % self.total_screens
            )
        elif button == LCDButton.DOWN:
            self.current_screen = Page(
                (self.current_screen.value + 1) % self.total_screens
            )
        else:
            self.update_display(button)

    def get_gps_data(self):
        try:
            report = self.session.next()
            if report["class"] == "TPV":
                return {
                    "latitude": getattr(report, "lat", "NA"),
                    "longitude": getattr(report, "lon", "NA"),
                    "altitude": getattr(report, "alt", "NA"),
                    "speed": getattr(report, "speed", "NA"),
                    "sats": len(getattr(report, "satellites", [])),
                    "time": getattr(report, "time", "NA"),
                }
        except (KeyError, StopIteration):
            return None

    def get_nearest_town(self) -> Waypoint:
        """Return the coordinates of the nearest town."""
        # TODO: Implement this
        return Waypoint(latitude=40.7128, longitude=-74.0060, altitude=10)

    def get_nearest_road(self) -> Waypoint:
        """Return the coordinates of the nearest road."""
        # TODO: Implement this
        return Waypoint(latitude=40.7128, longitude=-75.0060, altitude=10)

    def compass_heading(self, gps_data, destination) -> str:
        """Return the compass heading from the current location to the destination, ex 60 degrees east."""
        # TODO: Implement this
        return "Not Implemented"

    def update_display(self, button: Optional[LCDButton] = None) -> None:
        gps_data = self.get_gps_data()
        if gps_data is None:
            self.lcd_handler.display_text(["No GPS data"])
            return
        if self.current_screen == Page.TIME_AND_SATELLITES:
            self.display_time_and_satellites(gps_data, button)
        elif self.current_screen == Page.GPS_COORDINATES:
            self.display_gps_coordinates(gps_data, button)
        elif self.current_screen == Page.SELECT_DESTINATION:
            self.display_select_destination(button)
        elif self.current_screen == Page.SELECT_WAYPOINTS:
            self.display_select_waypoints(gps_data, button)
        elif self.current_screen == Page.COMPASS_HEADING_AND_SPEED:
            self.display_compass_heading_and_speed(gps_data, button)

    def display_time_and_satellites(
        self, gps_data, button: Optional[LCDButton] = None
    ) -> None:
        self.lcd_handler.display_text(
            [
                time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                f"Satellites: {gps_data['sats']}",
                f"Sync: {'Yes' if gps_data['time'] != 'NA' else 'No'}",
            ]
        )

    def display_gps_coordinates(
        self, gps_data, button: Optional[LCDButton] = None
    ) -> None:
        color = (
            (0, 255, 0)
            if gps_data["latitude"] != "NA" and gps_data["longitude"] != "NA"
            else (255, 0, 0)
        )
        self.lcd_handler.display_text(
            [f"Lat: {gps_data['latitude']}", f"Lon: {gps_data['longitude']}"],
            colors=[color, color],
        )

    def display_select_destination(self, button: Optional[LCDButton] = None) -> None:
        if button == LCDButton.KEY1:
            # Set the destination to the nearest town (mock implementation)
            self.saved_data.destination = self.get_nearest_town()
            self.save_data()
        elif button == LCDButton.KEY2:
            # Set the destination to the nearest road (mock implementation)
            self.saved_data.destination = self.get_nearest_road()
            self.save_data()
        elif button == LCDButton.KEY3:
            # Select the destination from a list of waypoints
            self.saved_data.destination = self.saved_data.waypoints[
                self.cur_waypoint_index
            ]
            self.save_data()

        if self.saved_data.destination:
            self.lcd_handler.display_text(
                [
                    f"Destination set to:",
                    f"Lat: {self.saved_data.destination.latitude}",
                    f"Lon: {self.saved_data.destination.longitude}",
                ]
            )
        else:
            self.lcd_handler.display_text(["No destination set"])

    def display_select_waypoints(
        self, gps_data, button: Optional[LCDButton] = None
    ) -> None:
        if button == LCDButton.SELECT:
            if gps_data["latitude"] != "NA" and gps_data["longitude"] != "NA":
                new_waypoint = Waypoint(
                    latitude=float(gps_data["latitude"]),
                    longitude=float(gps_data["longitude"]),
                    altitude=float(gps_data["altitude"]),
                )
                self.saved_data.waypoints.append(new_waypoint)
                self.save_data()
                self.lcd_handler.display_text(["Waypoint saved!"])
        elif button == LCDButton.KEY1:
            # Delete the current waypoint (confirmation can be added if needed)
            if self.saved_data.waypoints:
                del self.saved_data.waypoints[self.cur_waypoint_index]
                self.save_data()
                self.cur_waypoint_index = max(0, self.cur_waypoint_index - 1)
                self.lcd_handler.display_text(["Waypoint deleted!"])
            else:
                self.lcd_handler.display_text(["No waypoints saved"])
        elif button == LCDButton.KEY2:
            # Move to the previous waypoint
            self.cur_waypoint_index = (self.cur_waypoint_index - 1) % len(
                self.saved_data.waypoints
            )
        elif button == LCDButton.KEY3:
            # Move to the next waypoint
            self.cur_waypoint_index = (self.cur_waypoint_index + 1) % len(
                self.saved_data.waypoints
            )

        if self.saved_data.waypoints:
            waypoint = self.saved_data.waypoints[self.cur_waypoint_index]
            self.lcd_handler.display_text(
                [
                    f"Waypoint {self.cur_waypoint_index + 1}/{len(self.saved_data.waypoints)}",
                    f"Lat: {waypoint.latitude}",
                    f"Lon: {waypoint.longitude}",
                    f"Alt: {waypoint.altitude}",
                ]
            )
        else:
            self.lcd_handler.display_text(["No waypoints saved"])

    def display_compass_heading_and_speed(self, gps_data, button) -> None:
        if self.saved_data.destination:
            self.lcd_handler.display_text(
                [
                    f"Heading to: {self.saved_data.destination.latitude}, {self.saved_data.destination.longitude}",
                    f"Speed: {gps_data['speed']}",
                    f"Compass: {self.compass_heading(gps_data, self.saved_data.destination)}",
                ]
            )
        else:
            self.lcd_handler.display_text(["No destination set"])

    def main_loop(self) -> None:
        try:
            while True:
                self.update_display()
                time.sleep(1)
        except KeyboardInterrupt:
            pass  # gpiozero does not require explicit cleanup


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    # Create instances of the handlers
    lcd_handler = LCDHandler()
    gpio_handler = ButtonHandler(
        up_pin=KEY_UP_PIN,
        down_pin=KEY_DOWN_PIN,
        left_pin=KEY_LEFT_PIN,
        right_pin=KEY_RIGHT_PIN,
        select_pin=KEY_PRESS_PIN,
        key1_pin=KEY1_PIN,
        key2_pin=KEY2_PIN,
        key3_pin=KEY3_PIN,
    )
    gps_display = GPSDisplay(lcd_handler, gpio_handler)
    # start program run loop
    logging.info("Starting Main loop")
    gps_display.main_loop()


if __name__ == "__main__":
    main()
