import os

import pygame

from src.util import is_raspberrypi


class LEDStripController:
    def __init__(self):
        self.max_leds = 12
        self.pi = False
        self.displayinfo = None
        self.spritesheet = None
        self.displayinfo = None
        os.putenv('SDL_FBDEV', '/dev/fb0')
        pygame.init()
        self.displayinfo = pygame.display.Info()
        print(f"Display size = {self.displayinfo.current_w}x{self.displayinfo.current_h}")
        if not is_raspberrypi():
            self.lcd = pygame.display.set_mode((100, 1920))

    def cls(self):
        pass

    def on(self, led_index, colour=None):
        pass

    def off(self, led_index, colour=None):
        pass
