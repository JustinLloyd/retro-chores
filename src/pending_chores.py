from src.chore import Chore
from src.chore_handler_base import ChoreQueue
from util import ee


class PendingChores(ChoreQueue):
    def __init__(self):
        super().__init__('pending-chores.json')

    def pop(self)->Chore:
        chore = super().pop()
        print('pending-chore-popped', chore.task)
        ee.emit('pending-chore-popped', chore)
        return chore

    def push(self, chore:Chore):
        super().push(chore)
        print('pending-chore-pushed', chore.task)
        ee.emit('pending-chore-pushed', chore)

    def is_chore_pending(self, chore: Chore) -> bool:
        for pending_chore in self._chores:
            if pending_chore.hash == chore.hash:
                return True

        return False

    def count(self):
        return len(self._chores)
