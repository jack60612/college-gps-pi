import logging
from enum import Enum

from gpiozero import Button


class LCDButton(Enum):
    """Enum for the buttons on the LCD screen."""

    UP: int = 0
    DOWN: int = 1
    LEFT: int = 2
    RIGHT: int = 3
    SELECT: int = 4
    KEY1: int = 5
    KEY2: int = 6
    KEY3: int = 7


class ButtonHandler:

    def __init__(
        self,
        up_pin: int,
        down_pin: int,
        left_pin: int,
        right_pin: int,
        select_pin: int,
        key1_pin: int,
        key2_pin: int,
        key3_pin: int,
    ) -> None:
        self.up_button = Button(up_pin, pull_up=True)
        self.down_button = Button(down_pin, pull_up=True)
        self.left_button = Button(left_pin, pull_up=True)
        self.right_button = Button(right_pin, pull_up=True)
        self.select_button = Button(select_pin, pull_up=True)
        self.key1_button = Button(key1_pin, pull_up=True)
        self.key2_button = Button(key2_pin, pull_up=True)
        self.key3_button = Button(key3_pin, pull_up=True)

        logging.info("Button Handling initialized")

    def configure_callbacks(self, callback) -> None:
        self.up_button.when_pressed = lambda: callback(LCDButton.UP)
        self.down_button.when_pressed = lambda: callback(LCDButton.DOWN)
        self.left_button.when_pressed = lambda: callback(LCDButton.LEFT)
        self.right_button.when_pressed = lambda: callback(LCDButton.RIGHT)
        self.select_button.when_pressed = lambda: callback(LCDButton.SELECT)
        self.key1_button.when_pressed = lambda: callback(LCDButton.KEY1)
        self.key2_button.when_pressed = lambda: callback(LCDButton.KEY2)
        self.key3_button.when_pressed = lambda: callback(LCDButton.KEY3)
