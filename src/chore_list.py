from chore_handler_base import ChoreHandlerBase
from util import ee


class ChoreList(ChoreHandlerBase):
    def __init__(self, filename: str):
        super(ChoreList, self).__init__(filename)

    # def append(self, chore):
    #     self._chores.append(chore)
    #     self._save_chores()
    #     print('chore-added', chore.task)
    #     ee.emit('chore-added', chore)
    #
    # def remove(self, chore):
    #     self._chores.remove(chore)
    #     self._save_chores()
    #     print('chore-removed', chore.task)
    #     ee.emit('chore-removed', chore)
    #
