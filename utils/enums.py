from enum import Enum


class CronExpressions(Enum):

    EVERY_DAY_AT_11_45 = '45 11 * * *'
    EVERY_MINUTE = '* * * * *'
    # Add more enum members as needed
