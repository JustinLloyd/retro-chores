import hashlib
import time
from enum import IntEnum

import evt
from util import get_time, Period, Urgency, Daypart, Day, Month, ee


class Chore:
    def __init__(self):
        self.task = ""
        self.period = Period.DAILY
        self.dayparts = [Daypart.MORNING]
        self.urgency = Urgency.DAY
        self.occurences = []
        self.created_at = get_time()
        self.activated_at = None
        self.completed_at = None
        self.concluded_at = None
        self.display_position = None
        self.hash = self.calculate_hash(self)

    @staticmethod
    def calculate_hash(chore):
        return hashlib.md5(f'{chore.task}/{chore.period.name.lower()}/{chore.urgency.name.lower()}/{",".join([daypart.name.lower() for daypart in chore.dayparts])}'.encode('utf-8')).digest()

    def to_dict(self) -> dict:
        chore_data = {
            'task': self.task,
            'dayparts': [daypart.name.lower() for daypart in self.dayparts],
            'period': self.period.name.lower(),
            'urgency': self.urgency.name.lower(),
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'activated_at': self.activated_at,
            'concluded_at': self.concluded_at,
            'display_position': self.display_position
        }
        return chore_data

    def activate(self, display_position):
        if self.is_active():
            print("Tried to activate a chore that is already active", self.display_position, self.task)
            return

        self.display_position = display_position
        self.activated_at = get_time()
        print(('chore-activated', self.task))
        ee.emit(evt.CHORE_ACTIVATED, self)

    def complete(self):
        if self.is_complete():
            print("Tried to complete a chore that is already completed", self.display_position, self.task)
            return

        assert self.is_active()
        self.completed_at = get_time()
        print('chore-completed', self.task)
        ee.emit(evt.CHORE_COMPLETED, self)

    def uncomplete(self):
        if not self.is_complete():
            print("Tried to uncomplete a chore that hasn't been completed", self.display_position, self.task)
            return

        self.completed_at = None
        print('chore-uncompleted', self.task)
        ee.emit(evt.CHORE_UNCOMPLETED, self)

    def conclude(self):
        if not self.is_complete():
            print("Tried to conclude a chore that hasn't been completed", self.display_position, self.task)
            return

        self.concluded_at = get_time()
        self.display_position = None
        print('chore-concluded', self.task)
        ee.emit(evt.CHORE_CONCLUDED, self)

    def is_active(self):
        return self.activated_at is not None and self.completed_at is None

    def is_overdue(self):
        if self.activated_at is None:
            return False
        if self.completed_at is not None:
            return False
        timespan = get_time() - self.activated_at
        return timespan > 1000

    def is_complete(self):
        return self.completed_at is not None

    def is_concluded(self):
        if self.completed_at is None:
            return False
        timespan = get_time() - self.completed_at
        if timespan < 1000:
            return False
        return True

    @staticmethod
    def from_dict(chore_data: dict):
        chore = Chore()
        chore.period = Period.DAILY
        chore.urgency = Urgency.DAYPART
        chore.dayparts = [Daypart.MORNING]
        chore.occurences = []
        chore.task = chore_data['task']
        chore.created_at = chore_data['created_at'] if 'created_at' in chore_data else None
        chore.activated_at = chore_data['activated_at'] if 'activated_at' in chore_data else None
        chore.completed_at = chore_data['completed_at'] if 'completed_at' in chore_data else None
        chore.concluded_at = chore_data['concluded_at'] if 'concluded_at' in chore_data else None
        chore.display_position = chore_data['display_position'] if 'display_position' in chore_data else None

        if 'dayparts' in chore_data:
            chore.dayparts = []
            for daypart in chore_data['dayparts']:
                if daypart == 'morning':
                    chore.dayparts.append(Daypart.MORNING)
                elif daypart == 'afternoon':
                    chore.dayparts.append(Daypart.AFTERNOON)
                elif daypart == 'evening':
                    chore.dayparts.append(Daypart.EVENING)
                elif daypart == 'night':
                    chore.dayparts.append(Daypart.NIGHT)
                else:
                    print(f"Don't know what to do with {daypart} in {chore_data['task']}")

        if 'weekly' in chore_data:
            for occurence in chore_data['weekly']:
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
        elif 'monthly' in chore_data:
            for occurence in chore_data['monthly']:
                chore.occurences.append(int(occurence))
            chore.period = Period.MONTHLY
            chore.urgency = Urgency.WEEK
        elif 'yearly' in chore_data:
            for occurence in chore_data['yearly']:
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

        if 'urgency' in chore_data:
            if chore_data['urgency'] == 'immediate':
                chore.urgency = Urgency.IMMEDIATE
            elif chore_data['urgency'] == 'none':
                chore.urgency = Urgency.NONE
            elif chore_data['urgency'] == 'daypart':
                chore.urgency = Urgency.DAYPART
            elif chore_data['urgency'] == 'day':
                chore.urgency = Urgency.DAY
            elif chore_data['urgency'] == 'days':
                chore.urgency = Urgency.DAYS
            elif chore_data['urgency'] == 'week':
                chore.urgency = Urgency.WEEK
            elif chore_data['urgency'] == 'weeks':
                chore.urgency = Urgency.WEEKS
            elif chore_data['urgency'] == 'month':
                chore.urgency = Urgency.MONTH
            elif chore_data['urgency'] == 'months':
                chore.urgency = Urgency.MONTHS

        chore.hash = chore.calculate_hash(chore)
        return chore
