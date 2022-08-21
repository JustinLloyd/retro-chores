from enum import IntEnum


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
        chore_dict = {
            'task': self.task,
            'dayparts': [daypart.name.lower() for daypart in self.dayparts],
            'period': self.period.name.lower(),
            'urgency': self.urgency.name.lower()
        }
        return chore_dict

    @staticmethod
    def from_dict(chore_dict):
        chore = Chore()
        chore.period = Period.DAILY
        chore.urgency = Urgency.DAYPART
        chore.dayparts = [Daypart.MORNING]
        chore.occurences = []
        chore.task = chore_dict['task']
        if 'dayparts' in chore_dict:
            chore.dayparts = []
            for daypart in chore_dict['dayparts']:
                if daypart == 'morning':
                    chore.dayparts.append(Daypart.MORNING)
                elif daypart == 'afternoon':
                    chore.dayparts.append(Daypart.AFTERNOON)
                elif daypart == 'evening':
                    chore.dayparts.append(Daypart.EVENING)
                elif daypart == 'night':
                    chore.dayparts.append(Daypart.NIGHT)
                else:
                    print(f"Don't know what to do with {daypart} in {chore_dict['task']}")

        if 'weekly' in chore_dict:
            for occurence in chore_dict['weekly']:
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
        elif 'monthly' in chore_dict:
            for occurence in chore_dict['monthly']:
                chore.occurences.append(int(occurence))
            chore.period = Period.MONTHLY
            chore.urgency = Urgency.WEEK
        elif 'yearly' in chore_dict:
            for occurence in chore_dict['yearly']:
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

        if 'urgency' in chore_dict:
            if chore_dict['urgency'] == 'immediate':
                chore.urgency = Urgency.IMMEDIATE
            elif chore_dict['urgency'] == 'none':
                chore.urgency = Urgency.NONE
            elif chore_dict['urgency'] == 'daypart':
                chore.urgency = Urgency.DAYPART
            elif chore_dict['urgency'] == 'day':
                chore.urgency = Urgency.DAY
            elif chore_dict['urgency'] == 'days':
                chore.urgency = Urgency.DAYS
            elif chore_dict['urgency'] == 'week':
                chore.urgency = Urgency.WEEK
            elif chore_dict['urgency'] == 'weeks':
                chore.urgency = Urgency.WEEKS
            elif chore_dict['urgency'] == 'month':
                chore.urgency = Urgency.MONTH
            elif chore_dict['urgency'] == 'months':
                chore.urgency = Urgency.MONTHS

        return chore
