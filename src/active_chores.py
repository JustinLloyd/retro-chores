import json

import evt
import globals as g
from chore_array import ChoreArray
from chore import Chore
from util import ee


@ee.on(evt.BUTTON_TOGGLE_ON)
def toggle_switch_toggled_on(switch_index):
    g.chores.active_chores.on_toggle_switch_toggled_on(switch_index)


@ee.on(evt.BUTTON_TOGGLE_OFF)
def on_toggle_switch_toggled_off(switch_index):
    g.chores.active_chores.on_toggle_switch_toggled_off(switch_index)


@ee.on(evt.CHORE_COMPLETED)
def on_chore_completed(chore):
    g.chores.active_chores.on_chore_completed(chore)


@ee.on(evt.CHORE_UNCOMPLETED)
def on_chore_uncompleted(chore):
    g.chores.active_chores.on_chore_uncompleted(chore)


@ee.on(evt.CHORE_SKIPPED)
def on_chore_skipped(chore):
    raise NotImplemented


@ee.on(evt.CHORE_POSTPONED)
def on_chore_postponed(chore):
    raise NotImplemented


class ActiveChores(ChoreArray):
    def __init__(self):
        super().__init__('active-chores.json')

    def on_chore_completed(self, chore):
        super()._save_chores()

    def on_chore_uncompleted(self, chore):
        super()._save_chores()

    def on_toggle_switch_toggled_off(self, switch_index):
        self.uncomplete(switch_index)

    def on_toggle_switch_toggled_on(self, switch_index):
        self.complete(switch_index)

    def complete(self, index):
        chore = self.get(index)
        if chore is None:
            print("Tried to complete a non-existent chore", index)
            return

        chore.complete()
        print('active-chore-completed', index, chore.task)
        ee.emit(evt.ACTIVE_CHORE_COMPLETED, chore)

    def uncomplete(self, index):
        chore = self.get(index)
        if chore is None:
            print("Tried to uncomplete a non-existent chore", index)
            return

        chore.uncomplete()
        print('active-chore-uncompleted', index, chore.task)
        ee.emit(evt.ACTIVE_CHORE_UNCOMPLETED, chore)

    # skip a chore
    def skip(self):
        raise NotImplemented

    def postpone(self):
        raise NotImplemented

    # def append(self, chore: Chore):
    #     super().append(chore)
    #     print(evt.ACTIVE_CHORE_ADDED, chore.task)
    #     ee.emit(evt.ACTIVE_CHORE_APPENDED, chore)
    #
    # def remove(self, chore: Chore):
    #     super().remove(chore)
    #     print('active-chore-removed', chore.task)
    #     ee.emit(evt.ACTIVE_CHORED_REMOVED, chore)

    def is_chore_active(self, needle_chore: Chore) -> bool:
        for chore_in_haystack in self._chores:
            if chore_in_haystack is None:
                continue
            if chore_in_haystack.hash == needle_chore.hash:
                return True

        return False

    def conclude(self, chore):
        if not chore.is_complete():
            return
        chore.conclude()
        self._chores.remove(chore)
        print('active-chore-concluded', chore.task)
        ee.emit(evt.ACTIVE_CHORE_CONCLUDED, chore)

    def activate_chore(self, chore):
        empty_slot_index = self.find_empty_slot()
        chore.activate(empty_slot_index)
        self.append(chore)
        print('active-chore-activated', chore.task)
        ee.emit(evt.ACTIVE_CHORE_ACTIVATED, chore)

    def conclude_completed_chores(self):
        chores_to_conclude = []
        for chore in self._chores:
            if chore is None:
                continue
            if chore.is_complete():
                chores_to_conclude.append(chore)
        for chore in chores_to_conclude:
            chore.conclude()

    def get_incomplete_chores(self):
        return [chore for chore in self._chores if chore is not None and not chore.is_complete()]

    def get_active_chores(self):
        return [chore for chore in self._chores if chore is not None and chore.is_active()]