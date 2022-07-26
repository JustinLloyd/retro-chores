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
            if event.type == KEYDOWN and event.key == K_f:
                return


os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()

lcd = pygame.display.set_mode((320, 200))
lcd.fill((255, 0, 0))
pygame.display.update()
pygame.display.quit()
pygame.quit()
exit()
