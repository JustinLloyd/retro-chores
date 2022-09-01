
from chore import Chore
import cfg
from util import ee


@ee.on('chore-activated')
def add_chore_to_vfd(chore):
    cfg.chore_display.add_chore_to_vfd(chore)


class ChoreDisplay:
    def add_chore_to_vfd(self, chore):
        cfg.vfd.print(chore.task.upper(), chore.display_position)

    def remove_chore_from_vfd(self, chore: Chore):
        cfg.vfd.clr(chore.display_position)
