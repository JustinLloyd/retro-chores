import cfg

from util import ee
from toggle_button import ToggleSwitch


# TODO kinda shitty solution but it works for now
@ee.on('emulated-toggle-switch-toggled')
def emulated_toggle_switch_toggled(switch_index):
    cfg.toggle_switch_controller.toggle_emulated_switch(switch_index)


# this class handles the inpput, output and latching state of the toggle switches
class ToggleSwitchController:
    def __init__(self):
        self.toggle_switch_count = cfg.AVAILABLE_SLOTS
        self.displayinfo = None
        self.spritesheet = None
        # self.fake_switch = [False] * 12
        self.switches = []
        while len(self.switches) < cfg.AVAILABLE_SLOTS:
            self.switches.append(ToggleSwitch(len(self.switches)))

        if cfg.should_emulate_hardware():
            for switch in self.switches:
                switch.enable_emulation()

        self.switches_to_arm = []
        self.switches_to_disarm = []

        # if not is_raspberrypi():r
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
        for switch in self.switches:
            switch.refresh_state()

        while len(self.switches_to_arm) > 0:
            switch = self.switches_to_arm.pop()
            switch.arm()

        while len(self.switches_to_disarm) > 0:
            switch = self.switches_to_disarm.pop()
            switch.disarm()
            self.switches_to_arm.append(switch)

        # read state of all switches
        # for each switch
        # if state of switch changed
        pass

    def toggle_emulated_switch(self, switch_index: int):
        self.switches[switch_index].emulated_toggle()

    # TODO we probably want a function that will release the electromagnetic clamps, wait a few tens of milliseconds, and then re-engage the electromagnetic clamps
    # this function releases the electromagnetic clamps of all the toggle switches
    def reset_all(self):
        for switch in self.switches:
            self.switches_to_disarm.append(switch)
