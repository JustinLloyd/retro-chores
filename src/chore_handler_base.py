import json
import cfg

from src.chore import Chore
from util import ee


class ChoreHandlerBase:
    def __init__(self, filename: str):
        self.filename = filename
        self._chores = []
        self.__load_chores__()

    def __load_chores__(self):
        try:
            filepath = 'data/' + self.filename
            with open(filepath) as f:
                chore_data = json.load(f)
            f.close()
            self._chores = [Chore.from_dict(item) for item in chore_data['chores']]
        except Exception:
            self._chores = []
        # for item in chore_data['chores']:
        #     chore = Chore.from_dict(item)
        #     self.chores.append(chore)

    def _save_chores(self):
        chores_dict = {'chores': [chore.to_dict() for chore in self._chores if chore is not None and not chore.is_complete()]}
        try:
            filepath = 'data/' + self.filename
            with open(filepath, 'w') as f:
                json.dump(chores_dict, f, indent=4)
            f.close()
        except Exception:
            pass

    # def add(self, chore):
    #     self.chores.append(chore)
    #     self.__save_chores__()
    #
    # def remove(self, chore):
    #     self.chores.remove(chore)
    #     self.__save_chores__()
    #
    # def get(self, idx):
    #     return self.chores[idx]


class ChoreQueue(ChoreHandlerBase):
    def __init__(self, filename: str):
        super(ChoreQueue, self).__init__(filename)

    def push(self, chore: Chore):
        self._chores.append(chore)
        self._save_chores()
        print('chore-pushed', chore.task)
        ee.emit('chore-pushed', chore)

    def pop(self) -> Chore:
        chore = self._chores.pop(0)
        self._save_chores()
        print('chore-popped', chore.task)
        ee.emit('chore-popped', chore)
        return chore


class ChoreList(ChoreHandlerBase):
    def __init__(self, filename: str):
        super(ChoreList, self).__init__(filename)

    def append(self, chore):
        self._chores.append(chore)
        self._save_chores()
        print('chore-added', chore.task)
        ee.emit('chore-added', chore)

    def remove(self, chore):
        self._chores.remove(chore)
        self._save_chores()
        print('chore-remove', chore.task)
        ee.emit('chore-remove', chore)


class ChoreArray(ChoreHandlerBase):
    def __init__(self, filename: str):
        super(ChoreArray, self).__init__(filename)

    def append(self, chore):
        self._chores.append(chore)
        self._save_chores()
        print('chore-added', chore.task)
        ee.emit('chore-added', chore)

    def remove(self, chore):
        self._chores.remove(chore)
        self._save_chores()
        print('chore-removed', chore.task)
        ee.emit('chore-removed', chore)

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
    #     ee.emit('chore-added', chore)
    #     self._save_chores()

    def has_empty_slot(self):
        return len(self._chores) < cfg.AVAILABLE_SLOTS

    def find_empty_slot(self):
        # TODO randomize the empty slot selected if there is more than one empty slot
        if not self.has_empty_slot():
            raise RuntimeError('No available empty slot')

        slots = [idx for idx in range(cfg.AVAILABLE_SLOTS)]
        for chore in self._chores:
            slots.remove(chore.display_position)

        return slots[0]
