# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com
import os
from os import environ

from pyee import EventEmitter

import evt
import globals as g
from chore_display import ChoreDisplay
from chores_wrangler import ChoreWrangler
from toggle_switch_controller import ToggleSwitchController
from util import ee
import cfg
from virtual_vfd import VirtualVFD

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import sys
import pygame
from pygame.locals import *

is_running = True
joysticks = None


def game_loop():
    clock = pygame.time.Clock()
    while is_running:
        process_input()
        run_game_logic()
        update_display()
        clock.tick(60)


def run_game_logic():
    # rescan the known chores json
    g.chores.process_chore_logic()
    g.toggle_switch_controller.process_logic()
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


def process_joypad(event):
    if event.type == JOYBUTTONUP:
        button_index = event.button
        # was this a toggle switch that was flipped?
        if button_index >= cfg.BUTTON_TOGGLE_MIN and button_index <= cfg.BUTTON_TOGGLE_MAX:
            ee.emit(evt.BUTTON_TOGGLE_OFF, button_index)
        elif button_index >= cfg.BUTTON_POSTPONE_MIN and button_index <= cfg.BUTTON_POSTPONE_MAX:
            ee.emit(evt.BUTTON_POSTPONE_UP, button_index)
        elif button_index >= cfg.BUTTON_SKIP_MIN and button_index <= cfg.BUTTON_SKIP_MAX:
            ee.emit(evt.BUTTON_SKIP_UP, button_index)
        ee.emit(evt.BUTTON_UP, button_index)
        return

    if event.type == JOYBUTTONDOWN:
        button_index = event.button
        if button_index >= cfg.BUTTON_TOGGLE_MIN and button_index <= cfg.BUTTON_TOGGLE_MAX:
            ee.emit(evt.BUTTON_TOGGLE_ON, button_index)
        elif button_index >= cfg.BUTTON_POSTPONE_MIN and button_index <= cfg.BUTTON_POSTPONE_MAX:
            ee.emit(evt.BUTTON_POSTPONE_DOWN, button_index)
        elif button_index >= cfg.BUTTON_SKIP_MIN and button_index <= cfg.BUTTON_SKIP_MAX:
            ee.emit(evt.BUTTON_SKIP_DOWN, button_index)
        ee.emit(evt.BUTTON_DOWN, button_index)
        return


def process_keyboard(event):
    global is_running
    emulated_buttons = [K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12]
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            is_running = False
            return
        elif cfg.should_emulate_hardware():
            for button_index, emulated_button in enumerate(emulated_buttons):
                if event.key == emulated_button:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        ee.emit(evt.BUTTON_POSTPONE_DOWN, button_index)
                    elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                        ee.emit(evt.BUTTON_SKIP_DOWN, button_index)
                    else:
                        # toggle switches are a special case as they can "latch" so we emulate them by using a regular
                        # key down event to emulate the toggle switch being toggled on
                        ee.emit(evt.BUTTON_TOGGLE_ON, button_index)
                    ee.emit(evt.BUTTON_DOWN, button_index)
                    return
        return

    if event.type == KEYUP:
        if cfg.should_emulate_hardware():
            for button_index, emulated_button in enumerate(emulated_buttons):
                if event.key == emulated_button:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        ee.emit(evt.BUTTON_POSTPONE_UP, button_index)
                        ee.emit(evt.BUTTON_UP, button_index)
                    elif pygame.key.get_mods() & pygame.KMOD_RCTRL:
                        ee.emit(evt.BUTTON_SKIP_UP, button_index)
                        ee.emit(evt.BUTTON_UP, button_index)
                    elif pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        # and we toggle off the emulated toggle switch by using the keyup event but with the alt key modifier
                        ee.emit(evt.BUTTON_TOGGLE_OFF, button_index)
                        ee.emit(evt.BUTTON_UP, button_index)


def process_input():
    global is_running

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            is_running = False
        if event.type == JOYBUTTONUP or event.type == JOYBUTTONDOWN:
            process_joypad(event)
        if event.type == KEYDOWN or event.type == KEYUP:
            process_keyboard(event)


def update_display():
    pygame.display.update()


def init():
    global joysticks
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
    pygame.init()
    print('joystick count', pygame.joystick.get_count())
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    pygame.joystick.init()
    print(pygame.joystick.get_init())
    print(pygame.joystick.get_count())
    g.chores = ChoreWrangler()
    g.toggle_switch_controller = ToggleSwitchController()
    g.chore_display = ChoreDisplay()
    g.vfd = VirtualVFD()
    g.vfd.load_assets()
    g.vfd.cls()
    active_chores = g.chores.active_chores.get_active_chores()
    for chore in active_chores:
        print('chore-activated', chore.task)
        ee.emit(evt.CHORE_ACTIVATED, chore)


def shutdown():
    pygame.joystick.quit()
    pygame.display.quit()
    pygame.quit()


def main():
    init()
    game_loop()
    shutdown()


if __name__ == '__main__':
    main()
