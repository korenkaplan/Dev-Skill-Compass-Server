from usage_stats.models import HistoricalTechCounts, MonthlyTechnologiesCounts


def truncate_table():
    pass


def insert_from_historical_table(items: list[HistoricalTechCounts]):
    pass


def insert_from_monthly_table(items: list[MonthlyTechnologiesCounts]):
    pass



def refresh_aggregated_table(number_of_months: int):
    pass
