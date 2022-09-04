from chore import Chore
from chore_handler_base import ChoreHandlerBase
from util import ee


class ChoreQueue(ChoreHandlerBase):
    def __init__(self, filename: str):
        super(ChoreQueue, self).__init__(filename)

    def push(self, chore: Chore):
        super().append(chore)
        print('chore-pushed', chore.task)
        ee.emit('chore-pushed', chore)

    def pop(self) -> Chore:
        chore = self._chores.pop(0)
        self._save_chores()
        print('chore-popped', chore.task)
        ee.emit('chore-removed', chore)
        ee.emit('chore-popped', chore)
        return chore

