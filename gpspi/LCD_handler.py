import logging

from PIL import Image, ImageDraw, ImageFont

import gpspi.lcd.LCD_1in44 as LCD_1in44


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
        __current_brightness = max(0, self.__current_brightness - 5)
        self.__set_brightness(__current_brightness)

    def raise_brightness(self) -> None:
        __current_brightness = min(100, self.__current_brightness + 5)
        self.__set_brightness(__current_brightness)

    def reset_brightness(self) -> None:
        __current_brightness = 100
        self.__set_brightness(__current_brightness)

    def display_text(self, lines: list[str], colors=None) -> None:
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        y = 0
        for i, line in enumerate(lines):
            color = (255, 255, 255) if not colors else colors[i]
            self.draw.text((0, y), line, font=self.font, fill=color)
            y += 10
        self.disp.LCD_ShowImage(self.image, 0, 0)
