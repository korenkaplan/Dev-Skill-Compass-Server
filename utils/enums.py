from enum import Enum


class CronExpressions(Enum):

    EVERY_MONDAY_AT_10_10 = '10 10 * * 1'
    EVERY_DAY_AT_12_30 = '30 12 * * *'
    EVERY_FIRST_OF_MONTH_AT_4 = '0 4 1 * *'
    EVERY_MONDAY_AT_4 = '0 4 * * 1'
    EVERY_DAY_AT_10 = '0 10 * * *'
    # Add more enum members as needed
