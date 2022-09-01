from util import ee


class ToggleSwitch:
    def __init__(self, index: int):
        self.id = index
        self.emulated_state = False
        self.is_emulated = False
        self.state = False
        self.armed = False
        self.previous_armed = None
        self.previous_state = None

    def arm(self):
        self.previous_armed = self.armed
        self.armed = True
        if self.is_emulated:
            return

        # TODO write to the GPIO controller
        print('toggle-switch-armed', self.id)
        ee.emit('toggle-switch-armed', self.id)

    def disarm(self):
        self.previous_armed = self.armed
        self.armed = False
        if self.is_emulated:
            return

        # TODO write to the GPIO controller
        print('toggle-switch-disarmed', self.id)
        ee.emit('toggle-switch-disarmed', self.id)

    def enable_emulation(self):
        self.is_emulated = True

    def emulated_on(self):
        self.emulated_state = True

    def emulated_off(self):
        self.emulated_state = False

    def emulated_toggle(self):
        self.emulated_state = not self.state

    def refresh_state(self):
        self.previous_state = self.state
        if self.is_emulated:
            self.state = self.emulated_state
        else:
            # TODO read the GPIO controller state
            pass

        if self.state != self.previous_state:
            print('toggle-switch-toggled', self.id)
            ee.emit('toggle-switch-toggled', self.id)
            if self.state:
                print('toggle-switch-toggled-on', self.id)
                ee.emit('toggle-switch-toggled-on', self.id)
            else:
                print('toggle-switch-toggled-off', self.id)
                ee.emit('toggle-switch-toggled-off', self.id)

    def was_toggled_on(self):
        return not self.previous_state and self.state

    def was_toggled_off(self):
        return self.previous_state and not self.state

    def was_armed(self):
        return not self.previous_armed and self.armed

    def was_disarmed(self):
        return self.previous_armed and not self.armed
