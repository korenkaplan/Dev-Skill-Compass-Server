"""This module is a service class for """
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from usage_stats.models import MonthlyTechnologiesCounts, HistoricalTechCounts


# a function that: Gets all the rows from the monthly tech table and add them to the table.
def insert_rows_from_monthly_tech_table(tech_counts_list: list[MonthlyTechnologiesCounts]) -> list[HistoricalTechCounts]:
    inserted_rows = []
    # Add them to the table
    for tech_count in tech_counts_list:
        obj = HistoricalTechCounts.objects.create(role_id=tech_count.role_id, technology_id=tech_count.technology_id,
                                                  counter=tech_count.counter)
        inserted_rows.append(obj)

    return inserted_rows


# a functions that: gets all the data from the last x months by created_at field
def get_tech_counts_from_last_number_of_months(number_of_months: int) -> list[HistoricalTechCounts]:
    # get the date of today before months_number ago
    today = timezone.now()
    past_date = today - relativedelta(months=number_of_months)

    # get the list of rows where created at is larger than the date
    rows = HistoricalTechCounts.objects.filter(created_at__gte=past_date)

    return rows



