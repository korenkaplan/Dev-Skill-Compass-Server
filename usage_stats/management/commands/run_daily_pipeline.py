from django.core.cache import cache
from django.core.management.base import BaseCommand
from logic.pipelines.main import (
    thread_pool_role_pipline
)
from decorators.decorator_measure_function_time import measure_function_time
from utils.enums import GoogleJobsTimePeriod, LinkedinTimePeriod
from utils.functions import retry_function


class Command(BaseCommand):
    help = "Run the main pipeline"

    @measure_function_time
    def handle(self, *args, **options):
        # Call your initialization function here
        retry_function(daily_pipeline, role_name='daily_pipeline')
        # process_pool_role_pipline()
        self.stdout.write("run_daily_pipeline command executed")


def daily_pipeline():
    try:
        print("started daily pipeline...")
        # Define the time period
        google_period: GoogleJobsTimePeriod = GoogleJobsTimePeriod.WEEK
        linkedin_period: LinkedinTimePeriod = LinkedinTimePeriod.PAST_WEEK

        # Run the main pipeline with the period time set to one day
        thread_pool_role_pipline(google_period, linkedin_period)

        # Reset Cache
        cache.clear()

    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the daily pipeline: {e}"
        print(message)

