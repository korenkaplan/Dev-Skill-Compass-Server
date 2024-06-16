import os

from logic.pipelines.main import thread_pool_role_pipline_test, thread_pool_role_pipline
from utils.enums import GoogleJobsTimePeriod
from usage_stats.models import MonthlyTechnologiesCounts, AggregatedTechCounts
from usage_stats.services.aggregated_tech_counts_service import insert_from_monthly_table
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from utils.enums import LinkedinTimePeriod
from utils.functions import write_text_to_file

# Determine the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the log file
log_file_path = os.path.join(project_root, "Logs", "weekly_pipeline.log.txt")


def weekly_pipeline():
    try:
        # Define the time period
        period: GoogleJobsTimePeriod = GoogleJobsTimePeriod.WEEK
        linkedin_period: LinkedinTimePeriod = LinkedinTimePeriod.PAST_WEEK

        # Run the main pipeline with the period time set to one day
        # Run the main pipeline with the period time set to one week
        thread_pool_role_pipline(period, linkedin_period)

        # Get the min date
        today = timezone.now()
        past_date = today - relativedelta(days=2)

        # Get the monthly counts from the last scan
        items: list[MonthlyTechnologiesCounts] = MonthlyTechnologiesCounts.objects.filter(created_at__gte=past_date)

        # Update the aggregated table
        inserted_items: list[AggregatedTechCounts] = insert_from_monthly_table(items)

        print(f"Total amount inserted successfully: {len(inserted_items)}")

    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the monthly pipeline: {e}"
        write_text_to_file(log_file_path, 'a', message)


def weekly_pipeline_test():
    try:
        # Define the time period
        period: GoogleJobsTimePeriod = GoogleJobsTimePeriod.MONTH

        # Run the main pipeline with the period time set to one week
        thread_pool_role_pipline_test(period)

        # Get the min date
        today = timezone.now()
        past_date = today - relativedelta(days=2)

        # Get the monthly counts from the last scan
        items: list[MonthlyTechnologiesCounts] = MonthlyTechnologiesCounts.objects.filter(created_at__gte=past_date)

        # Update the aggregated table
        inserted_items: list[AggregatedTechCounts] = insert_from_monthly_table(items)

        print(f"Total amount inserted successfully: {len(inserted_items)}")

    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the monthly pipeline: {e}"
        write_text_to_file(log_file_path, 'a', message)
