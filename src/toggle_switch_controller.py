import pygame

from src.util import is_raspberrypi


# this class handles the inpput, output and latching state of the toggle switches
class ToggleSwitchController:
    def __init__(self, isPi):
        self.toggle_switch_count = 12
        self.displayinfo = None
        self.spritesheet = None

        if not is_raspberrypi():
            self.toggle_display = pygame.display.set_mode((100, 1920))

    # TODO we probably want a function that will release the electromagnetic clamps, wait a few tens of milliseconds, and then re-engage the electromagnetic clamps
    # this function releases the electromagnetic clamps of all the toggle switches
    def cls(self):
        for i in range(0, self.toggle_switch_count):
            self.release_clamp(i)

    # this function releases the electromagnetic clamp of the specified toggle switch, throwing the toggle switch automatically to the off position
    def release_clamp(self, switch_index):
        # TODO verify switch index is in range
        if is_raspberrypi():
            # write the GPIO pins that will release the electromagnetic clamps
            pass
        else:
            # update the virtual toggle switch display
            pass
        pass

    # this function will engage the electromagnetic clamp on the toggle switch permitting it to latch in the on position.
    def engage_clamp(self, switch_index):
        # TODO verify switch index is in range
        if is_raspberrypi():
            # write the GPIO pins that will engage the electormagnetic clamps
            pass
        else:
            # update the virtual toggle switch display
            pass
