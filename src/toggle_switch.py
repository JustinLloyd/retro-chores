from util import ee


class ToggleSwitch:
    def __init__(self, index: int):
        self.id = index
        self.emulated_toggle_state = False
        self.is_emulated = False
        self.toggle_state = False
        self.armed_state = False
        self.previous_armed_state = None
        self.previous_toggle_state = None

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
        ee.emit('toggle-switch-armed', self.id)

    def disarm(self):
        self.previous_armed_state = self.armed_state
        self.armed_state = False
        if not self.is_emulated:
            # TODO write to the GPIO controller
            pass

        print('toggle-switch-disarmed', self.id)
        ee.emit('toggle-switch-disarmed', self.id)

    def enable_emulation(self):
        self.is_emulated = True

    def emulated_on(self):
        self.emulated_toggle_state = True

    def emulated_off(self):
        self.emulated_toggle_state = False

    def emulated_toggle(self):
        self.emulated_toggle_state = not self.toggle_state

    def refresh_state(self):
        self.previous_toggle_state = self.toggle_state
        if self.is_emulated:
            self.toggle_state = self.emulated_toggle_state
            if not self.armed_state:
                self.emulated_toggle_state = False
        else:
            # TODO read the GPIO controller state
            pass

        if self.toggle_state != self.previous_toggle_state:
            print('toggle-switch-toggled', self.id)
            ee.emit('toggle-switch-toggled', self.id)
            if self.toggle_state:
                print('toggle-switch-toggled-on', self.id)
                ee.emit('toggle-switch-toggled-on', self.id)
            else:
                print('toggle-switch-toggled-off', self.id)
                ee.emit('toggle-switch-toggled-off', self.id)

    def was_toggled_on(self):
        return not self.previous_toggle_state and self.toggle_state

    def was_toggled_off(self):
        return self.previous_toggle_state and not self.toggle_state

    def is_armed(self):
        return self.armed_state

    def was_armed(self):
        return not self.previous_armed_state and self.armed_state

    def was_disarmed(self):
        return self.previous_armed_state and not self.armed_state
