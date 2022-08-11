import json
from enum import IntEnum
import jsonpickle


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
    def __init__(self, task=None, period=None, urgency=None):
        self.task = task
        self.period = Period.DAILY
        self.dayparts = [Daypart.MORNING]
        self.urgency = Urgency.DAY
        self.occurences = []

    def to_json(self):
        pass

    @staticmethod
    def from_json(json):
        chore = Chore()
        chore.period = Period.DAILY
        chore.urgency = Urgency.DAYPART
        chore.dayparts = [Daypart.MORNING]
        chore.occurences = []
        chore.task = json['task']
        if 'dayparts' in json:
            chore.dayparts = []
            for daypart in json['dayparts']:
                if daypart == 'morning':
                    chore.dayparts.append(Daypart.MORNING)
                elif daypart == 'afternoon':
                    chore.dayparts.append(Daypart.AFTERNOON)
                elif daypart == 'evening':
                    chore.dayparts.append(Daypart.EVENING)
                elif daypart == 'night':
                    chore.dayparts.append(Daypart.NIGHT)
                else:
                    print(f"Don't know what to do with {daypart} in {json['task']}")

        if 'weekly' in json:
            for occurence in json['weekly']:
                if occurence == 'sunday':
                    chore.occurences.append(Day.SUNDAY)
                elif occurence == 'sunday':
                    chore.occurences.append(Day.MONDAY)
                elif occurence == 'sunday':
                    chore.occurences.append(Day.TUESDAY)
                elif occurence == 'sunday':
                    chore.occurences.append(Day.WEDNESDAY)
                elif occurence == 'sunday':
                    chore.occurences.append(Day.THURSDAY)
                elif occurence == 'sunday':
                    chore.occurences.append(Day.FRIDAY)
                elif occurence == 'sunday':
                    chore.occurences.append(Day.SATURDAY)
            chore.period = Period.WEEKLY
            chore.urgency = Urgency.DAY
        elif 'monthly' in json:
            for occurence in json['monthly']:
                chore.occurences.append(int(occurence))
            chore.period = Period.MONTHLY
            chore.urgency = Urgency.WEEK
        elif 'yearly' in json:
            for occurence in json['yearly']:
                if occurence == 'january':
                    chore.occurences.append(Month.JANUARY)
                elif occurence == 'february':
                    chore.occurences.append(Month.FEBRUARY)
                elif occurence == 'march':
                    chore.occurences.append(Month.MARCH)
                elif occurence == 'april':
                    chore.occurences.append(Month.APRIL)
                elif occurence == 'may':
                    chore.occurences.append(Month.MAY)
                elif occurence == 'june':
                    chore.occurences.append(Month.JUNE)
                elif occurence == 'july':
                    chore.occurences.append(Month.JULY)
                elif occurence == 'august':
                    chore.occurences.append(Month.AUGUST)
                elif occurence == 'september':
                    chore.occurences.append(Month.SEPTEMBER)
                elif occurence == 'october':
                    chore.occurences.append(Month.OCTOBER)
                elif occurence == 'november':
                    chore.occurences.append(Month.NOVEMBER)
                elif occurence == 'december':
                    chore.occurences.append(Month.DECEMBER)
            chore.period = Period.YEARLY
            chore.urgency = Urgency.MONTH

        if 'urgency' in json:
            if json['urgency'] == 'immediate':
                chore.urgency = Urgency.IMMEDIATE
            elif json['urgency'] == 'none':
                chore.urgency = Urgency.NONE
            elif json['urgency'] == 'daypart':
                chore.urgency = Urgency.DAYPART
            elif json['urgency'] == 'day':
                chore.urgency = Urgency.DAY
            elif json['urgency'] == 'days':
                chore.urgency = Urgency.DAYS
            elif json['urgency'] == 'week':
                chore.urgency = Urgency.WEEK
            elif json['urgency'] == 'weeks':
                chore.urgency = Urgency.WEEKS
            elif json['urgency'] == 'month':
                chore.urgency = Urgency.MONTH
            elif json['urgency'] == 'months':
                chore.urgency = Urgency.MONTHS

        return chore


class ChoreWrangler:
    def __init__(self):
        self.urgency_names = [e.name.lower() for e in Urgency]
        self.daypart_names = [e.name.lower() for e in Daypart]
        self.day_names = [e.name.lower() for e in Day]
        self.month_names = [e.name.lower() for e in Month]
        self.period_names = [e.name.lower() for e in Period]
        self.active_chores = None

        with open('chores.json') as f:
            data = json.load(f)
        f.close()

        self.known_chores = []
        print(data['chores'])
        for choreJson in data['chores']:
            chore = Chore.from_json(choreJson)
            print(chore.task)
            self.known_chores.append(chore)

        # self.pending_chores = PendingChores()
        # self.active_chores = ActiveChores()
        # self.concluded_chores = ConcludedChores()

    def skip(self):
        # remove chore from active chore list
        # add chore to concluded chore list
        pass

    def load_active_chores(self):
        return None

    def load_chores(self):
        self.active_chores = self.load_active_chores()
        # load the active chores list
        # load the concluded chores list
        # load the pending chores list
        # load the known chores list

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
