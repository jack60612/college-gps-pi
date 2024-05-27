import logging
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

import gpspi.lcd.LCD_1in44 as LCD_1in44
from gpspi.types.page import Page


class LCDHandler:
    def __init__(self) -> None:
        # Initialize the display
        self.disp: LCD_1in44.LCD = LCD_1in44.LCD()
        self.disp.LCD_Init(LCD_1in44.SCAN_DIR_DFT)
        self.disp.LCD_Clear()

        # Create an image to display
        self.width: int = self.disp.width
        self.height: int = self.disp.height
        self.__current_brightness: int = 100
        self.image: Image.Image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

        logging.info("LCD initialized")

    def __set_brightness(self, level: int) -> None:
        self.disp.bl_DutyCycle(level)

    def lower_brightness(self) -> None:
        __current_brightness = max(0, self.__current_brightness - 10)
        self.__set_brightness(__current_brightness)

    def raise_brightness(self) -> None:
        __current_brightness = min(100, self.__current_brightness + 10)
        self.__set_brightness(__current_brightness)

    def reset_brightness(self) -> None:
        __current_brightness = 100
        self.__set_brightness(__current_brightness)

    def display_text(
        self,
        page_number: Page,
        lines: list[str],
        colors: Optional[list[tuple[int, int, int]]] = None,
        buttons: Optional[list[str]] = None,
    ) -> None:
        # Make max line length 20 characters, raise error
        for line in lines:
            if len(line) > 20:
                raise ValueError("Line too long")
        # page number on top,
        lines.insert(0, f"Page {page_number.value}")
        if colors is not None:
            colors.insert(0, (255, 255, 255))  # make page number white, stops error

        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        y = 0
        for i, line in enumerate(lines):
            color = (255, 255, 255) if not colors else colors[i]
            self.draw.text((0, y), line, font=self.font, fill=color)
            y += 10

        # also add 3 button messages for left side
        if buttons is not None:
            # draw from other side
            for i, button in enumerate(buttons):
                self.draw.text(
                    (self.width - 20, (((self.height - 25) * i) / 3) + 25), button, font=self.font, fill=(255, 255, 255)
                )

        self.disp.LCD_ShowImage(self.image, 0, 0)
