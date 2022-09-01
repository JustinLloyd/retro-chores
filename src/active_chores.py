import json

from src.chore import Chore
from src.chore_handler_base import ChoreArray
from util import ee


class ActiveChores(ChoreArray):
    def __init__(self):
        super().__init__('active-chores.json')

    def complete(self):
        raise NotImplemented

    def uncomplete(self):
        raise NotImplemented

    # skip a chore
    def skip(self):
        raise NotImplemented

    def postpone(self):
        raise NotImplemented

    def append(self, chore:Chore):
        super().append(chore)
        print('active-chore-added', chore.task)
        ee.emit('active-chore-added', chore)

    def remove(self, chore: Chore):
        super().remove(chore)
        print('active-chore-removed', chore.task)
        ee.emit('active-chore-removed', chore)

    def is_chore_active(self, needle_chore: Chore) -> bool:
        for chore_in_haystack in self._chores:
            if chore_in_haystack is None:
                continue
            if chore_in_haystack.hash == needle_chore.hash:
                return True

        return False

    def conclude(self, chore):
        chore.conclude()
        self._chores.remove(chore)
        ee.emit('active-chore-concluded', chore)

    def conclude_completed_chores(self):
        chores_to_conclude = []
        for chore in self._chores:
            if chore is None:
                continue
            if chore.is_complete():
                chores_to_conclude.append(chore)
        for chore in chores_to_conclude:
            chore.conclude()
        ee.emit('concluded-completed-chores', chores_to_conclude)

    def get_incomplete_chores(self):
        return [chore for chore in self._chores if chore is not None and not chore.is_complete()]

    def get_active_chores(self):
        return [chore for chore in self._chores if chore is not None and chore.is_active()]