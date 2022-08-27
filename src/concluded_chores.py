from chore import Chore
from src.chore_handler_base import ChoreList
from util import get_time


class ConcludedChores(ChoreList):
    def __init__(self):
        super().__init__('concluded-chores.json')

    def clean_up(self):
        for chore in self._chores:
            timespan = get_time() - chore.concluded_at
            if timespan > 1000:
                self._chores.remove(chore)

    def append(self, chore: Chore):
        chore.concluded_at = get_time()
        chore.completed_at = None
        self._chores.append(chore)
