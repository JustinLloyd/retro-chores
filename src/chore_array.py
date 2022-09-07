import cfg
from chore_handler_base import ChoreHandlerBase
from util import ee


class ChoreArray(ChoreHandlerBase):
    def __init__(self, filename: str):
        super(ChoreArray, self).__init__(filename)

    # def append(self, chore):
    #     self._chores.append(chore)
    #     self._save_chores()
    #     print('chore-added', chore.task)
    #     ee.emit(evt.CHORE_ADDED, chore)
    #
    # def remove(self, chore):
    #     self._chores.remove(chore)
    #     self._save_chores()
    #     print('chore-removed', chore.task)
    #     ee.emit(evt.CHORE_REMOVED, chore)

    def get(self, position: int):
        if position < 0 or position >= cfg.AVAILABLE_SLOTS:
            raise RuntimeError('Position is out of range')

        for chore in self._chores:
            if chore.display_position == position:
                return chore
        return None

    # def put(self, chore: Chore):
    #     if chore is None:
    #         raise RuntimeError("Chore cannot be empty")
    #     if chore.display_position is None:
    #         raise RuntimeError("Chore's display position cannot be empty")
    #     if chore.display_position < 0 or chore.display_position > 11:
    #         raise RuntimeError("Chore's display position must be between 0 and 11")
    #
    #     self._chores[chore.display_position] = chore
    #     ee.emit(evt.CHORE_ADDED, chore)
    #     self._save_chores()

    def has_empty_slot(self):
        return self.count() < cfg.AVAILABLE_SLOTS

    def find_empty_slot(self):
        # TODO randomize the empty slot selected if there is more than one empty slot
        if not self.has_empty_slot():
            raise RuntimeError('No available empty slot')

        slots = [idx for idx in range(cfg.AVAILABLE_SLOTS)]
        if len(self._chores) > 0:
            for chore in self._chores:
                slots.remove(chore.display_position)

        return slots[0]
