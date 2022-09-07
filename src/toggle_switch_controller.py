import cfg
import evt
import globals as g

from util import ee
from toggle_switch import ToggleSwitch


# TODO kinda shitty solution but it works for now
@ee.on(evt.CHORE_ACTIVATED)
def on_chore_activated(chore):
    g.toggle_switch_controller.on_chore_activated(chore)


# this class handles latching state of the electromagnetic toggle switches
class ToggleSwitchController:
    def __init__(self):
        # self.fake_switch = [False] * 12
        self.switches = []
        while len(self.switches) < cfg.BUTTON_TOGGLE_MAX:
            self.switches.append(ToggleSwitch(len(self.switches)))

        if cfg.should_emulate_hardware():
            for switch in self.switches:
                switch.enable_emulation()

        self.switches_to_arm = []
        # self.switches_to_disarm = []

        # if not is_raspberrypi():r
        #     self.toggle_display = pygame.display.set_mode((100, 1920))

    def on_chore_activated(self, chore):
        self.arm(chore.display_position)

    def get(self, index):
        assert index >= cfg.BUTTON_TOGGLE_MIN and index < cfg.BUTTON_TOGGLE_MAX
        return self.switches[index]

    # def is_down(self, index):
    #     assert index >= cfg.BUTTON_TOGGLE_MIN and index < cfg.BUTTON_TOGGLE_MAX
    #     return self.switches[index].is_down()
    #
    # def is_up(self, index):
    #     assert index >= cfg.BUTTON_TOGGLE_MIN and index < cfg.BUTTON_TOGGLE_MAX
    #     return self.switches[index].is_up()

    def arm(self, index):
        assert index >= cfg.BUTTON_TOGGLE_MIN and index < cfg.BUTTON_TOGGLE_MAX
        if self.switches[index].is_armed():
            print('Toggle switch is already armed', index)
            return

        self.switches[index].arm()
        print('toggle-switch-controller-arm', index)
        ee.emit(evt.TOGGLE_SWITCH_CONTROLLER_ARM, index)

    def disarm(self, index):
        assert index >= cfg.BUTTON_TOGGLE_MIN and index < cfg.BUTTON_TOGGLE_MAX
        self.switches[index].disarm()
        print('toggle-switch-controller-disarm', index)
        ee.emit(evt.TOGGLE_SWITCH_CONTROLLER_DISARM, index)

    def reset(self, index):
        assert index >= cfg.BUTTON_TOGGLE_MIN and index < cfg.BUTTON_TOGGLE_MAX
        self.disarm(index)
        self.switches_to_arm.append(self.switches[index])
        raise NotImplemented

    def process_logic(self):
        # for switch in self.switches:
        #     switch.refresh_state()
        #
        while len(self.switches_to_arm) > 0:
            switch = self.switches_to_arm.pop()
            switch.arm()

        # while len(self.switches_to_disarm) > 0:
        #     switch = self.switches_to_disarm.pop()
        #     switch.disarm()
        #     self.switches_to_arm.append(switch)

        # read state of all switches
        # for each switch
        # if state of switch changed
        pass

    # this function releases the electromagnetic clamps of all the toggle switches and then schedules them to be re-armed in one game frame
    def reset_all(self):
        for switch in self.switches:
            self.switches_to_arm.append(switch)
            switch.disarm()

        ee.emit(evt.TOGGLE_SWITCH_CONTROLLER_RESET_ALL)
