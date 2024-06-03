""" The pipeline that happens at the start of every month"""

from usage_stats.models import MonthlyTechnologiesCounts
from usage_stats.services.historical_tech_counts_service import (
    insert_rows_from_monthly_tech_table,
    get_tech_counts_from_last_number_of_months
)
from usage_stats.services.aggregated_tech_counts_service import truncate_table, insert_from_historical_table


def monthly_pipeline(number_of_months):
    """
    Executes the monthly pipeline to move data from the MonthlyTechnologiesCounts table to the HistoricalTechCounts table,
    and updates the aggregated counts table with the latest data from the last `number_of_months` months.

    Args:
        number_of_months (int): The number of months to include in the aggregated counts.

    Raises:
        ValueError: If `number_of_months` is not a positive integer.
    """
    if number_of_months <= 0:
        raise ValueError("number_of_months must be a positive integer")

    try:
        # Get all the rows from the monthly tech counts table
        technology_counts = MonthlyTechnologiesCounts.objects.all()

        # Insert them into the historical data table
        inserted_objects = insert_rows_from_monthly_tech_table(technology_counts)

        # Truncate the monthly stats table
        MonthlyTechnologiesCounts.objects.all().delete()

        # Insert the rows from historical data table from the last number of months to the aggregated table
        historical_tech_counts = get_tech_counts_from_last_number_of_months(number_of_months)

        # Truncate the aggregated table
        truncate_table()

        # Insert the counts from historical counts
        insert_from_historical_table(historical_tech_counts)

    except Exception as e:
        # Log the error or handle it as needed
        print(f"An error occurred during the monthly pipeline: {e}")
        raise
