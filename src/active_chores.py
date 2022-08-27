from src.chore import Chore
from src.chore_handler_base import ChoreArray


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

    def remove(self, chore: Chore):
        try:
            index = self._chores.index(chore)
            self._chores[index] = None
        except ValueError:
            pass

    def is_chore_active(self, needle_chore: Chore) -> bool:
        for chore_in_haystack in self._chores:
            if chore_in_haystack is None:
                continue
            if chore_in_haystack.hash == needle_chore.hash:
                return True

        return False

    def clean_up_old_chores(self):
        old_chores = []
        for chore in self._chores:
            if chore is None:
                continue
            if chore.is_complete():
                self._chores.remove(chore)
                old_chores.append(chore)
        return old_chores

    def get_incomplete_chores(self):
        return [chore for chore in self._chores if chore is not None and not chore.is_complete()]

    def get_active_chores(self):
        return [chore for chore in self._chores if chore is not None and chore.is_active()]