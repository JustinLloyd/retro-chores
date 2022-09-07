import evt
import globals as g
from chore_list import ChoreList
from util import get_time, ee


@ee.on(evt.CHORE_CONCLUDED)
def on_chore_concluded(chore):
    g.chores.concluded_chores.on_chore_concluded(chore)


class ConcludedChores(ChoreList):
    def __init__(self):
        super().__init__('concluded-chores.json')

    def on_chore_concluded(self, chore):
        self.conclude_chore(chore)

    def clean_up(self):
        for chore in self._chores:
            timespan = get_time() - chore.concluded_at
            # TODO fix this - don't alter the chores list while enumerating, you will get unexpected side effects
            if timespan > 1000:
                self._chores.remove(chore)

    def conclude_chore(self, chore):
        chore.concluded_at = get_time()
        self._chores.append(chore)
        ee.emit(evt.CHORE_CONCLUDED, chore)
