import evt
from util import ee


class ToggleSwitch:
    def __init__(self, index: int):
        self.armed_state = False
        self.previous_armed_state = None
        self.id = index
        self.is_emulated = False

    def enable_emulation(self):
        self.is_emulated = True

    def disable_emulation(self):
        self.is_emulated = False

    def arm(self):
        if self.armed_state:
            print('Toggle switch is already armed', self.id)
            return

        self.previous_armed_state = self.armed_state
        self.armed_state = True
        if not self.is_emulated:
            # TODO write to the GPIO controller
            pass

        print('toggle-switch-armed', self.id)
        ee.emit(evt.TOGGLE_SWITCH_ARMED, self.id)

    def disarm(self):
        self.previous_armed_state = self.armed_state
        self.armed_state = False
        if not self.is_emulated:
            # TODO write to the GPIO controller
            pass

        print('toggle-switch-disarmed', self.id)
        ee.emit(evt.TOGGLE_SWITCH_DISARMED, self.id)

    def is_armed(self):
        return self.armed_state

    def was_armed(self):
        return not self.previous_armed_state and self.armed_state

    def was_disarmed(self):
        return self.previous_armed_state and not self.armed_state
