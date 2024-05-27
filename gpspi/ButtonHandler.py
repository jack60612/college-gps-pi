from enum import Enum
from gpiozero import Button


class LCDButton(Enum):
    """Enum for the buttons on the LCD screen."""

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    SELECT = 4
    KEY1 = 5
    KEY2 = 6
    KEY3 = 7


class ButtonHandler:

    def __init__(
        self,
        up_pin,
        down_pin,
        left_pin,
        right_pin,
        select_pin,
        key1_pin,
        key2_pin,
        key3_pin,
    ):
        self.up_button = Button(up_pin, pull_up=True)
        self.down_button = Button(down_pin, pull_up=True)
        self.left_button = Button(left_pin, pull_up=True)
        self.right_button = Button(right_pin, pull_up=True)
        self.select_button = Button(select_pin, pull_up=True)
        self.key1_button = Button(key1_pin, pull_up=True)
        self.key2_button = Button(key2_pin, pull_up=True)
        self.key3_button = Button(key3_pin, pull_up=True)

    def configure_callbacks(self, callback):
        self.up_button.when_pressed = lambda: callback(LCDButton.UP)
        self.down_button.when_pressed = lambda: callback(LCDButton.DOWN)
        self.left_button.when_pressed = lambda: callback(LCDButton.LEFT)
        self.right_button.when_pressed = lambda: callback(LCDButton.RIGHT)
        self.select_button.when_pressed = lambda: callback(LCDButton.SELECT)
        self.key1_button.when_pressed = lambda: callback(LCDButton.KEY1)
        self.key2_button.when_pressed = lambda: callback(LCDButton.KEY2)
        self.key3_button.when_pressed = lambda: callback(LCDButton.KEY3)
