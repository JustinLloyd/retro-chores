import json
import queue
from array import array

import numpy as numpy

from src.chore import Chore


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

    def pop(self) -> Chore:
        chore = self._chores.pop(0)
        self._save_chores()
        return chore


class ChoreList(ChoreHandlerBase):
    def __init__(self, filename: str):
        super(ChoreList, self).__init__(filename)

    def append(self, chore):
        self._chores.append(chore)

    def remove(self, chore):
        self._chores.remove(chore)


class ChoreArray(ChoreHandlerBase):
    def __init__(self, filename: str, size: int = 12):
        super(ChoreArray, self).__init__(filename)
        while len(self._chores) < size:
            self._chores.append(None)
        # self.chores = numpy.empty(size, dtype=Chore)
        # chores = self.__load_chores__()
        # try:
        #     for idx, chore in enumerate(chores):
        #         self.chores[idx] = chore
        # except Exception:
        #     pass

    def get(self, index: int) -> Chore:
        return self._chores[index]

    def put(self, chore: Chore):
        if chore is None:
            raise RuntimeError("Chore cannot be empty")
        if chore.display_position is None:
            raise RuntimeError("Chore's display position cannot be empty")
        if chore.display_position < 0 or chore.display_position>11:
            raise RuntimeError("Chore's display position must be between 0 and 11")

        self._chores[chore.display_position] = chore
        self._save_chores()

    def has_empty_slot(self):
        if None in self._chores:
            return True
        return False

    def find_empty_slot(self):
        # TODO randomize the empty slot selected if there is more than one empty slot
        return self._chores.index(None)
