""" The pipeline that happens at the start of every month"""
import os

from usage_stats.models import MonthlyTechnologiesCounts
from usage_stats.services.historical_tech_counts_service import insert_rows_from_monthly_tech_table
from usage_stats.services.aggregated_tech_counts_service import refresh_aggregated_table
from utils.functions import write_text_to_file


# Determine the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the log file
log_file_path = os.path.join(project_root, "Logs", "monthly_pipeline.log.txt")


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
        insert_rows_from_monthly_tech_table(technology_counts)

        # Truncate the monthly stats table
        MonthlyTechnologiesCounts.objects.all().delete()

        # Refresh the table
        refresh_aggregated_table(number_of_months)

    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the monthly pipeline: {e}"
        write_text_to_file(log_file_path, 'a', message)


