import globals as g
from chore_queue import ChoreQueue
from src.chore import Chore
from util import ee


class PendingChores(ChoreQueue):
    def __init__(self):
        super().__init__('pending-chores.json')

    def is_chore_pending(self, chore: Chore) -> bool:
        for pending_chore in self._chores:
            if pending_chore.hash == chore.hash:
                return True

        return False
