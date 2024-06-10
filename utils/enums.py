from enum import Enum


class CronExpressions(Enum):

    EVERY_DAY_AT_11_45 = '45 11 * * *'
    EVERY_MINUTE = '* * * * *'
    # Add more enum members as needed


class LinkedinTimePeriod(Enum):
    PAST_MONTH = "r2592000"
    PAST_WEEK = "r604800"
    PAST_24_HOURS = "r86400"
