import globals as g
from momentary_switch import MomentarySwitch


class MomentarySwitchController:
    def __init__(self):
        self.switches = []
        while len(self.switches) < 5:
            self.switches.append(MomentarySwitch())
