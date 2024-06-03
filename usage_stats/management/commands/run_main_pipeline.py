from django.core.management.base import BaseCommand
from logic.pipelines.main import (
    process_pool_role_pipline, process_pool_role_pipline_test,
)
from decorators.decorator_measure_function_time import measure_function_time
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod


class Command(BaseCommand):
    help = "Run the main pipeline"

    @measure_function_time
    def handle(self, *args, **options):
        # Call your initialization function here
        process_pool_role_pipline_test(GoogleJobsTimePeriod.WEEK)
        # process_pool_role_pipline()
        self.stdout.write("run_main_pipeline command executed")
