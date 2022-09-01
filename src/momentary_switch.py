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

