import datetime
import time
import io
from enum import IntEnum

import pygame.time

pi = False
platform_confirmed = False
use_accelerated_time = True
use_fixed_start_time = True
emulated_hardware = True
real_hardware_available = False
clean_up_chores = True


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
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


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


def get_daypart(time):
    hour = time.hour
    if hour >= 5 and hour <= 11:
        return Daypart.MORNING
    if hour >= 12 and hour <= 16:
        return Daypart.AFTERNOON
    if hour >= 17 and hour <= 19:
        return Daypart.EVENING
    if hour >= 20:
        return Daypart.NIGHT
    return Daypart.NONE


def get_datetime():
    if use_fixed_start_time:
        return datetime.datetime(2022, 8, 25, 10, 0, 0)
    return datetime.datetime.now()


def get_time():
    if use_accelerated_time:
        return datetime.datetime(2022, 8, 25, 10, 0, 0).timestamp() + pygame.time.get_ticks() * 600
    return time.time()


def has_real_hardware():
    return real_hardware_available


def should_emulate_hardware():
    return emulated_hardware


def should_clean_up_chores():
    return clean_up_chores


def is_raspberrypi():
    global platform_confirmed
    global pi
    if platform_confirmed:
        return pi

    try:
        platform_confirmed = True
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower():
                pi = True
                return True
    except Exception:
        pass
    return False
