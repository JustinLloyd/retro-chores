import cfg
from chore import Chore
from chore_list import ChoreList
from util import get_time, ee


@ee.on('chore-concluded')
def on_chore_concluded(chore):
    concluded_chores.on_chore_concluded(chore)


class ConcludedChores(ChoreList):
    def __init__(self):
        global concluded_chores
        super().__init__('concluded-chores.json')
        concluded_chores = self

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
        ee.emit('concluded-chore', chore)


concluded_chores: ConcludedChores
