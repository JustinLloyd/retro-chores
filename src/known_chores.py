import globals as g
from chore_list import ChoreList
from util import get_datetime, Period, get_daypart


class KnownChores(ChoreList):
    def __init__(self):
        super().__init__('chores.json')

    def get_new_pending_chores(self) -> list:
        current_daypart = get_daypart(get_datetime())

        pending_chores = []
        for chore in self._chores:
            if chore.period == Period.DAILY:
                if current_daypart in chore.dayparts:
                    pending_chores.append(chore)

        return pending_chores
