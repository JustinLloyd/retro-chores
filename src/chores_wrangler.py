# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com
import copy
import time
import datetime

import globals as g
from src.active_chores import ActiveChores
from src.concluded_chores import ConcludedChores
from src.known_chores import KnownChores
from src.pending_chores import PendingChores
from util import get_datetime, Daypart, Urgency, Day, Month, Period, get_daypart, get_time, ee


class ChoreWrangler:
    def __init__(self):
        self.urgency_names = [e.name.lower() for e in Urgency]
        self.daypart_names = [e.name.lower() for e in Daypart]
        self.day_names = [e.name.lower() for e in Day]
        self.month_names = [e.name.lower() for e in Month]
        self.period_names = [e.name.lower() for e in Period]
        self.active_chores = ActiveChores()
        self.known_chores = KnownChores()
        self.pending_chores = PendingChores()
        self.concluded_chores = ConcludedChores()

    # TODO when a chore is completed, it is added to the concluded chores list, but not removed from the active chores list
    # TODO when a chore is completed and becomes stale after a time, it is simply removed from the active chore list - no further processing takes place as it is already on the the concluded chores list
    # TODO we might want to rename concluded chores list to completed chores list
    # TODO on start we want to unlatch all toggle switches by default

    # def complete_chore(self, index):
    #     self.active_chores.complete(index)
    #
    # def uncomplete_chore(self, index):
    #     self.active_chores.uncomplete(index)

    def process_chore_logic(self):
        # convert now into a daypart
        # convert now into a day of month
        # convert now into a day of week
        # convert now into a month
        # now = datetime.datetime.now()
        now = get_datetime()

        current_daypart = get_daypart(now)

        possible_pending_chores = self.known_chores.get_new_pending_chores()
        for chore in possible_pending_chores:
            if self.active_chores.is_chore_active(chore):
                continue
            if self.pending_chores.is_chore_pending(chore):
                continue

            pending_chore = copy.deepcopy(chore)
            pending_chore.created_at = get_time()
            self.pending_chores.push(chore)
            break

        # move pending chores to active chores if there are empty slots on the active chores list
        self.process_pending_chores()

        # TODO remove expired chores from the active chore list
        # TODO tell the toggle switch to reset itself
        # TODO tell the VFD to update itself
        # TODO add a flag to the chore to indicate it has been completed
        # TODO add a time to the chore to indicate when it was completed
        # TODO change visual status of chore if it has been on the active list too long
        # TODO change visual status of chore if it has been completed
        # TODO act a function to the chore to determine if it has been completed
        # TODO add a function to the chore to determine if it is overdue
        # TODO add a function to the chore to determine if it should be scheduled (added to the pending list)
        # TODO consider switching to event emitters for many things, e.g. adding chores, moving chores between lists, etc
        # if a chore is already on the active chore list, don't process it
        # if a chore is already on the pending chore list, don't process it
        # once per hour
        #   run through known chores list
        #   look for any chore that has a daypart/day/week/whatever that falls within the current hour
        #   if that chore isn't on the active/pending list, then add the chore to the pending list

        # if there is empty slots on the active list, move a chore from the pending list to the active list
        # an example:
        # it is 5AM on monday morning and we have a weekly chore that occurs on Monday, Wednesday & Friday.
        # we hash the chore
        # then we go through all the chores on the pending & active list to determine if that chore is already in the queue

    def skip(self):
        # remove chore from active chore list
        # add chore to concluded chore list
        pass

    def process_pending_chores(self):
        if not self.active_chores.has_empty_slot():
            return

        if self.pending_chores.count() == 0:
            return

        chore = self.pending_chores.pop()
        self.active_chores.activate_chore(chore)
