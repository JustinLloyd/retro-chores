# All code, images, text and other artifacts are copyright 2022 Justin Lloyd
# All Rights Reserved
# https://justin-lloyd.com
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
    def __init__(self):
        self.task = ""
        self.period = Period.DAILY
        self.dayparts = [Daypart.MORNING]
        self.urgency = Urgency.DAY
        self.occurences = []

    def to_dict(self):
        dict = {'task': self.task}
        dict['dayparts'] = [daypart.name.lower() for daypart in self.dayparts]
        dict['period'] = self.period.name.lower()
        dict['urgency'] = self.urgency.name.lower()
        return dict

    @staticmethod
    def from_dict(dict):
        chore = Chore()
        chore.period = Period.DAILY
        chore.urgency = Urgency.DAYPART
        chore.dayparts = [Daypart.MORNING]
        chore.occurences = []
        chore.task = dict['task']
        if 'dayparts' in dict:
            chore.dayparts = []
            for daypart in dict['dayparts']:
                if daypart == 'morning':
                    chore.dayparts.append(Daypart.MORNING)
                elif daypart == 'afternoon':
                    chore.dayparts.append(Daypart.AFTERNOON)
                elif daypart == 'evening':
                    chore.dayparts.append(Daypart.EVENING)
                elif daypart == 'night':
                    chore.dayparts.append(Daypart.NIGHT)
                else:
                    print(f"Don't know what to do with {daypart} in {dict['task']}")

        if 'weekly' in dict:
            for occurence in dict['weekly']:
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
        elif 'monthly' in dict:
            for occurence in dict['monthly']:
                chore.occurences.append(int(occurence))
            chore.period = Period.MONTHLY
            chore.urgency = Urgency.WEEK
        elif 'yearly' in dict:
            for occurence in dict['yearly']:
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

        if 'urgency' in dict:
            if dict['urgency'] == 'immediate':
                chore.urgency = Urgency.IMMEDIATE
            elif dict['urgency'] == 'none':
                chore.urgency = Urgency.NONE
            elif dict['urgency'] == 'daypart':
                chore.urgency = Urgency.DAYPART
            elif dict['urgency'] == 'day':
                chore.urgency = Urgency.DAY
            elif dict['urgency'] == 'days':
                chore.urgency = Urgency.DAYS
            elif dict['urgency'] == 'week':
                chore.urgency = Urgency.WEEK
            elif dict['urgency'] == 'weeks':
                chore.urgency = Urgency.WEEKS
            elif dict['urgency'] == 'month':
                chore.urgency = Urgency.MONTH
            elif dict['urgency'] == 'months':
                chore.urgency = Urgency.MONTHS

        return chore


class ChoreWrangler:
    def __init__(self):
        self.urgency_names = [e.name.lower() for e in Urgency]
        self.daypart_names = [e.name.lower() for e in Daypart]
        self.day_names = [e.name.lower() for e in Day]
        self.month_names = [e.name.lower() for e in Month]
        self.period_names = [e.name.lower() for e in Period]
        self.active_chores = []
        self.known_chores = []

        self.load_all_chores()
        print(self.known_chores[0].to_dict())
        self.add_active(self.known_chores[0])
        # self.pending_chores = PendingChores()
        # self.active_chores = ActiveChores()
        # self.concluded_chores = ConcludedChores()

    def skip(self):
        # remove chore from active chore list
        # add chore to concluded chore list
        pass

    def load_all_chores(self):
        self.load_known_chores()
        self.load_active_chores()

    def load_known_chores(self):
        self.load_chores(self.known_chores, 'chores.json')

    def load_active_chores(self):
        self.load_chores(self.active_chores, 'active-chores.json')

    @staticmethod
    def load_chores(chores, filename):
        with open(filename) as f:
            chore_data = json.load(f)
        f.close()

        chores.clear()
        for item in chore_data['chores']:
            chore = Chore.from_dict(item)
            chores.append(chore)


        # load the active chores list
        # load the concluded chores list
        # load the pending chores list
        # load the known chores list

    def add_pending(self):
        pass

    def get_pending(self):
        pass

    def remove_pending(self):
        pass

    def add_active(self, chore):
        self.active_chores.append(chore)
        self.save_active_chores()

    def remove_active(self):
        pass

    def complete_active(self):
        pass

    def undo_active(self):
        pass

    @staticmethod
    def save_chores(chores, filename):
        chores_dict = {'chores': [chore.to_dict() for chore in chores]}

        with open(filename, 'w') as f:
            json.dump(chores_dict, f, indent=4)
        f.close()

    def save_active_chores(self):
        self.save_chores(self.active_chores, 'active-chores.json')

    def save_all_chores(self):
        self.save_active_chores()