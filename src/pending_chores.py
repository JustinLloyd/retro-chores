from src.chore import Chore
from src.chore_handler_base import ChoreQueue


class PendingChores(ChoreQueue):
    def __init__(self):
        super().__init__('pending-chores.json')

    def is_chore_pending(self, chore: Chore) -> bool:
        for pending_chore in self._chores:
            if pending_chore.hash == chore.hash:
                return True

        return False

    def count(self):
        return len(self._chores)
