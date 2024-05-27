from django.core.management.base import BaseCommand
from logic.main_pipeline.main import process_pool_role_pipline
from decorators.messure_function_time_dec import measure_function_time


class Command(BaseCommand):
    help = 'Run the main pipeline'

    @measure_function_time
    def handle(self, *args, **options):
        # Call your initialization function here
        process_pool_role_pipline()
        self.stdout.write("run_main_pipeline command executed")
