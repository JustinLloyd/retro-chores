import json
from enum import IntEnum


class ActiveChores:
    def __init__(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass

    def complete(self):
        pass

    def uncomplete(self):
        pass

    # skip a chore
    def skip(self):
        pass


class PendingChores:
    def __init__(self):
        pass


class ConcludedChores:
    def __init__(self):
        self.chores = []
        pass

    def add(self):
        pass

    def clean_up(self):
        pass


class Urgency(IntEnum):
    NONE = 0
    IMMEDIATE = 1
    DAYPART = 2
    DAY = 3
    DAYS = 4
    WEEK = 5
    WEEKS = 6
    MONTH = 7
    MONTHS = 8


class Daypart(IntEnum):
    NONE = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4


class Day(IntEnum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7


class Month(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class Period(IntEnum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4


class Chore:
    def __init__(self, task):
        self.urgency_names = [e.name.lower() for e in Urgency]
        self.daypart_names = [e.name.lower() for e in Daypart]
        self.day_names = [e.name.lower() for e in Day]
        self.month_names = [e.name.lower() for e in Month]
        self.period_names = [e.name.lower() for e in Period]
        self.task = task
        self.period=Period.DAILY
        self.daypart = Daypart.MORNING
        self.urgency = Urgency.DAY


class ChoreWrangler:
    def __init__(self):
        with open('chores.json') as f:
            data = json.load(f)
        f.close()

        print(data['chores'])
        # self.pending_chores = PendingChores()
        # self.active_chores = ActiveChores()
        # self.concluded_chores = ConcludedChores()

    def skip(self):
        # remove chore from active chore list
        # add chore to concluded chore list
        pass

    def load_chores(self):
        # load the active chores list
        # load the concluded chores list
        # load the pending chores list
        # load the known chores list
        pass

    def save_chores(self):
        pass

    def add_pending(self):
        pass

    def get_pending(self):
        pass

    def remove_pending(self):
        pass

    def add_active(self):
        pass

    def remove_active(self):
        pass

    def complete_active(self):
        pass

    def undo_active(self):
        pass
