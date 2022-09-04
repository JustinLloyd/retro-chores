# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com
import os
from os import environ

from pyee import EventEmitter

from chore_display import ChoreDisplay
from src.chores_wrangler import ChoreWrangler
from src.led_strip_controller import LEDStripController
from src.virtual_vfd import VirtualVFD
from toggle_switch_controller import ToggleSwitchController
from util import ee
import cfg



environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
import pygame
from pygame.locals import *

is_running = True

def game_loop():
    clock = pygame.time.Clock()
    while is_running:
        process_input()
        run_game_logic()
        update_display()
        clock.tick(60)


def run_game_logic():
    # rescan the known chores json
    cfg.chores.process_chore_logic()
    cfg.toggle_switch_controller.process_logic()
    # for idx in updated_slots:
    #     active_chore = chores.active_chores.get(idx)
    #     if active_chore is None:
    #         vfd.clr(idx)
    #         # disarm the toggle switch
    #         # turn off the green LED
    #     else:
    #          activate_chore(active_chore)
    #         # arm the to ggle switch
    #         # illuminate the red LED
    # # remove chores from concluded chores list
    # # add new pending chores
    # # add new active chores
    # pass

def process_input():
    global is_running

    emulated_buttons = [K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12]
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            is_running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                is_running = False
        if event.type == KEYUP:
            for index, emulated_button in enumerate(emulated_buttons):
                if event.key == emulated_button:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        ee.emit('emulated-momentary-switch-postponed', index)
                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        ee.emit('emulated-momentary-switch-skipped', index)
                    else:
                        ee.emit('emulated-toggle-switch-toggled', index)


def update_display():
    pygame.display.update()


def init():
    if cfg.should_clean_up_chores():
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
    cfg.chores = ChoreWrangler()
    cfg.toggle_switch_controller = ToggleSwitchController()
    cfg.chore_display = ChoreDisplay()
    pygame.init()
    cfg.vfd = VirtualVFD()
    cfg.vfd.load_assets()
    cfg.vfd.cls()
    active_chores = cfg.chores.active_chores.get_active_chores()
    for chore in active_chores:
        print('chore-activated', chore.task)
        ee.emit('chore-activated', chore)


def shutdown():
    pygame.display.quit()
    pygame.quit()


def main():
    init()
    game_loop()
    shutdown()


if __name__ == '__main__':
    main()
