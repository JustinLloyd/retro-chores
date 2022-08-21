# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com

from src.active_chores import ActiveChores
from src.chore import Urgency, Daypart, Day, Month, Period, Chore
from src.concluded_chores import ConcludedChores
from src.known_chores import KnownChores
from src.pending_chores import PendingChores


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

        self.active_chores.add(self.known_chores.chores[0])

    def skip(self):
        # remove chore from active chore list
        # add chore to concluded chore list
        pass

