import sys

import pygame
import os

from pygame.locals import *


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()

displayinfo = pygame.display.Info()
if (displayinfo.current_w==1100):
    lcd = pygame.display.set_mode((1100, 3840))
else:
    lcd = pygame.display.set_mode((550, 1920))

lcd.fill((255, 0, 0))
pygame.display.update()
wait()
pygame.display.quit()
pygame.quit()
exit()
