# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com
import os
from os import environ

from src.chores_wrangler import ChoreWrangler
from src.led_strip_controller import LEDStripController
from src.vfd import VFD
from util import should_clean_up_chores

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
import pygame
from pygame.locals import *

vfd: VFD
chores: ChoreWrangler
vLEDStrip: LEDStripController


def game_loop():
    clock = pygame.time.Clock()
    while True:
        process_input()
        run_game_logic()
        update_display()
        clock.tick(60)


def run_game_logic():
    # rescan the known chores json
    updated_slots = chores.process_chore_logic()
    for idx in updated_slots:
        active_chore = chores.active_chores.get(idx)
        if active_chore is None:
            vfd.clr(idx)
            # disarm the toggle switch
            # turn off the green LED
        else:
            activate_chore(active_chore)
            # arm the to ggle switch
            # illuminate the red LED
    # remove chores from concluded chores list
    # add new pending chores
    # add new active chores
    pass


def process_input():
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                shutdown()
        if event.type == KEYUP:

            if event.key == K_F1:
                # complete task #1
                pass


def activate_chore(chore):
    vfd.print(chore.task.upper(), chore.display_position)


def update_display():
    pygame.display.update()


def init():
    global vfd
    global chores

    if should_clean_up_chores():
        os.makedirs('./data', exist_ok=True)
        if os.path.exists('./data/active-chores.json'):
            os.remove('./data/active-chores.json')
        if os.path.exists('./data/concluded-chores.json'):
            os.remove('./data/concluded-chores.json')
        if os.path.exists('./data/pending-chores.json'):
            os.remove('./data/pending-chores.json')

    os.putenv('SDL_FBDEV', '/dev/fb0')
    if pygame.get_sdl_version()[0] < 2:
        raise SystemExit("This application requires pygame 2 and SDL2.")
    chores = ChoreWrangler()
    pygame.init()
    vfd = VFD()
    vfd.load_assets()
    vfd.cls()
    active_chores = chores.active_chores.get_active_chores()
    for chore in active_chores:
        activate_chore(chore)


def shutdown():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def main():
    init()

    # for count, chore in enumerate(chores.known_chores._chores):
    #     vfd.print(chore.task.upper(), count)
    #     print(chore.task.upper(), count)

    # vfd.flush()
    game_loop()


if __name__ == '__main__':
    main()
