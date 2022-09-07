import cfg
import evt
from chore import Chore
from util import ee
import globals as g

@ee.on(evt.CHORE_ACTIVATED)
def on_chore_activated(chore):
    g.chore_display.on_chore_activated(chore)


class ChoreDisplay:
    def __init__(self):
        pass

    def on_chore_activated(self, chore):
        self.add_chore_to_vfd(chore)

    def add_chore_to_vfd(self, chore):
        g.vfd.print(chore.task.upper(), chore.display_position)

    def remove_chore_from_vfd(self, chore: Chore):
        g.vfd.clr(chore.display_position)
