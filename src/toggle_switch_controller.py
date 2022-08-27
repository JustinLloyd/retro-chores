from enum import IntEnum

import pygame

from src.util import is_raspberrypi


class GPIOOutputHandler:
    pass


class GPIOInputHandler:
    pass


class ToggleSwitch:
    def __init__(self):
        self.state = False
        self.armed = False

    def arm(self):
        raise NotImplemented

    def disarm(self):
        raise NotImplemented


class MomentarySwitch:
    def __init__(self):
        self.state = False

    def is_down(self):
        raise NotImplemented

    def is_up(self):
        raise NotImplemented

    def was_pressed(self):
        raise NotImplemented

    def was_released(self):
        raise NotImplemented


class MomentarySwitchController:
    def __init__(self):
        self.switches = []
        while len(self.switches) < 5:
            self.switches.append(MomentarySwitch())


# this class handles the inpput, output and latching state of the toggle switches
class ToggleSwitchController:
    def __init__(self):
        self.toggle_switch_count = 12
        self.displayinfo = None
        self.spritesheet = None
        self.fake_switch = [False] * 12
        self.switches = []
        while len(self.switches) < 12:
            self.switches.append(ToggleSwitch())

        self.switches_to_arm = []
        self.switches_to_disarm = []

        # if not is_raspberrypi():
        #     self.toggle_display = pygame.display.set_mode((100, 1920))

    def get(self, index):
        return self.switches[index]

    def arm_by_index(self, index):
        self.switches[index].arm()

    def disarm_by_index(self, index):
        self.switches[index].disarm()

    def reset_by_index(self, index):
        self.switches_to_disarm.append(self.switches[index])
        raise NotImplemented

    def process_logic(self):
        while len(self.switches_to_arm) > 0:
            switch = self.switches_to_arm.pop()
            switch.arm()

        while len(self.switches_to_disarm) > 0:
            switch = self.switches_to_disarm.pop()
            switch.disarm()
            self.switches_to_arm.append(switch)

        pass

    # TODO we probably want a function that will release the electromagnetic clamps, wait a few tens of milliseconds, and then re-engage the electromagnetic clamps
    # this function releases the electromagnetic clamps of all the toggle switches
    def reset_all(self):
        for switch in self.switches:
            self.switches_to_disarm.append(switch)
