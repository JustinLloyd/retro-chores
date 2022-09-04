import json

import cfg
from chore_array import ChoreArray
from src.chore import Chore
from util import ee


@ee.on('toggle-switch-toggled-on')
def toggle_switch_toggled_on(switch_index):
    active_chores.on_toggle_switch_toggled_on(switch_index)


@ee.on('toggle-switch-toggled-off')
def on_toggle_switch_toggled_off(switch_index):
    active_chores.on_toggle_switch_toggled_off(switch_index)


@ee.on('chore-completed')
def on_chore_completed(chore):
    active_chores.on_chore_completed(chore)


@ee.on('chore-uncompleted')
def on_chore_uncompleted(chore):
    active_chores.on_chore_uncompleted(chore)


@ee.on('chore-skipped')
def chore_skipped(chore):
    raise NotImplemented


@ee.on('chore-postponed')
def chore_postponed(chore):
    raise NotImplemented


class ActiveChores(ChoreArray):
    def __init__(self):
        global active_chores
        super().__init__('active-chores.json')
        active_chores = self

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
        ee.emit('active-chore-completed', chore)

    def uncomplete(self, index):
        chore = self.get(index)
        if chore is None:
            print("Tried to uncomplete a non-existent chore", index)
            return

        chore.uncomplete()
        print('active-chore-uncompleted', index, chore.task)
        ee.emit('active-chore-uncompleted', chore)

    # skip a chore
    def skip(self):
        raise NotImplemented

    def postpone(self):
        raise NotImplemented

    # def append(self, chore: Chore):
    #     super().append(chore)
    #     print('active-chore-added', chore.task)
    #     ee.emit('active-chore-appended', chore)
    #
    # def remove(self, chore: Chore):
    #     super().remove(chore)
    #     print('active-chore-removed', chore.task)
    #     ee.emit('active-chore-removed', chore)

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
        ee.emit('active-chore-concluded', chore)

    def activate_chore(self, chore):
        empty_slot_index = self.find_empty_slot()
        chore.activate(empty_slot_index)
        self.append(chore)
        print('active-chore-activated', chore.task)
        ee.emit('active-chore-activated', chore)

    def conclude_completed_chores(self):
        chores_to_conclude = []
        for chore in self._chores:
            if chore is None:
                continue
            if chore.is_complete():
                chores_to_conclude.append(chore)
        for chore in chores_to_conclude:
            chore.conclude()
        # ee.emit('active-chore-concluded-chores', chores_to_conclude)

    def get_incomplete_chores(self):
        return [chore for chore in self._chores if chore is not None and not chore.is_complete()]

    def get_active_chores(self):
        return [chore for chore in self._chores if chore is not None and chore.is_active()]

active_chores:ActiveChores