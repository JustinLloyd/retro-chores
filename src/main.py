# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com
import os
import io
from os import environ

from src.chores import ChoreWrangler
from src.led_strip_controller import LEDStripController
from src.vfd import VFD

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
import pygame
from pygame.locals import *

pi = False

vfd: VFD
vLEDStrip: LEDStripController


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


def init():
    global vfd
    os.putenv('SDL_FBDEV', '/dev/fb0')
    if pygame.get_sdl_version()[0] < 2:
        raise SystemExit("This application  requires pygame 2 and SDL2.")

    pygame.init()
    vfd = VFD()
    vfd.load_assets()
    vfd.cls()


init()
chores = ChoreWrangler()

for count, chore in enumerate(chores.known_chores.chores):
    vfd.print(chore.task.upper(), count)
    print(chore.task.upper(), count)
# vfd.print('CLEAN UPSTAIRS\nCAT LITTER', 1)
# vfd.print('WATER BASIL PLANTS', 2)
# vfd.print('WATER ROSEMARY PLANT', 3)
# vfd.print('ADVANCE LAUNDRY', 4)
# vfd.print('EMPTY DISHWASHER', 5)
# vfd.print('LOAD DISHWASHER', 6)
# vfd.print('EMPTY RECYCLING BIN', 7)
# vfd.print('WASH MICROWAVE', 8)
# vfd.print('CHANGE BED LINENS', 9)

vfd.flush()
wait()
pygame.display.quit()
pygame.quit()
exit()
