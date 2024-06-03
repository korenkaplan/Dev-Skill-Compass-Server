""" The pipline that happeneds every start of a month"""
from usage_stats.models import MonthlyTechnologiesCounts
from usage_stats.services.historical_tech_counts_service import (insert_rows_from_monthly_tech_table,
                                                                 get_tech_counts_from_last_number_of_months)


def monthly_pipeline(number_of_months):
    # Get all the rows from the monthly tech counts table
    technology_counts = MonthlyTechnologiesCounts.objects.all()

    # insert them into the historical data table
    inserted_objects = insert_rows_from_monthly_tech_table(technology_counts)

    # truncate the monthly stats table
    MonthlyTechnologiesCounts.objects.all().delete()

    # insert the rows from historical data table from the last number of months to the aggregated table
    historical_tech_counts = get_tech_counts_from_last_number_of_months(number_of_months)

    # Refresh the aggregated table

