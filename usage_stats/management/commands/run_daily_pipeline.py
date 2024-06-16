from django.core.management.base import BaseCommand
from logic.pipelines.main import (
    thread_pool_role_pipline
)
from decorators.decorator_measure_function_time import measure_function_time
from utils.enums import GoogleJobsTimePeriod


class Command(BaseCommand):
    help = "Run the main pipeline"

    @measure_function_time
    def handle(self, *args, **options):
        # Call your initialization function here
        thread_pool_role_pipline(GoogleJobsTimePeriod.TODAY)
        # process_pool_role_pipline()
        self.stdout.write("run_main_pipeline command executed")
