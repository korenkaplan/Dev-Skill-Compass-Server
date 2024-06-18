""" The pipeline that happens at the start of every month"""
import os

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from django.utils import timezone
from usage_stats.models import MonthlyTechnologiesCounts, AggregatedTechCounts, HistoricalTechCounts
from utils.functions import write_text_to_file
from utils.settings import NUMBER_OF_MONTHS_TO_AGGREGATE

# Determine the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the log file
log_file_path = os.path.join(project_root, "Logs", "monthly_pipeline.log.txt")


def monthly_pipeline():
    """
    Executes the monthly pipeline to move data from the MonthlyTechnologiesCounts table to
     the HistoricalTechCounts table,
    and updates the aggregated counts table with the latest data from the last `number_of_months` months.

    Raises:
        ValueError: If `number_of_months` is not a positive integer.
    """
    number_of_months = NUMBER_OF_MONTHS_TO_AGGREGATE
    if number_of_months <= 0:
        raise ValueError("number_of_months must be a positive integer")

    try:
        # Get all the rows from the monthly tech counts table
        technology_counts: QuerySet[MonthlyTechnologiesCounts] = MonthlyTechnologiesCounts.objects.all()

        # Insert them into the historical data table
        for row in technology_counts:
            HistoricalTechCounts.objects.create(technology_id=row.technology_id, role_id=row.role_id, counter=row.counter)

        # Truncate the monthly stats table
        MonthlyTechnologiesCounts.objects.all().delete()

        # Truncate the aggregated stats table
        AggregatedTechCounts.objects.all().delete()


        # get the date of today before months_number ago
        today = timezone.now()
        past_date = today - relativedelta(months=number_of_months)

        # get the list of rows where created at is larger than the date
        rows: QuerySet[HistoricalTechCounts] = HistoricalTechCounts.objects.filter(created_at__gte=past_date)

        # insert the rows into the empty aggregated table
        for row in rows:
            # See if there is already a count of this Tech & Role combination
            object_in_db: AggregatedTechCounts = AggregatedTechCounts.objects.filter(role_id=row.role_id, technology_id=row.technology_id).first()

            # if exist update the count (To merge same counts from different months)
            if object_in_db:
                object_in_db.counter += row.counter
                object_in_db.save()

            # if not exist create the object
            else:
                AggregatedTechCounts.objects.create(technology_id=row.technology_id, role_id=row.role_id, counter=row.counter)


    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the monthly pipeline: {e}"
        write_text_to_file(log_file_path, 'a', message)
