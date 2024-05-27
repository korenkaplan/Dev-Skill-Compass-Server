from django.core.management.base import BaseCommand
from logic.main_pipeline.main import process_pool_role_pipline


class Command(BaseCommand):
    help = 'Run the main pipeline'

    def handle(self, *args, **options):
        # Call your initialization function here
        process_pool_role_pipline()
        self.stdout.write("run_main_pipeline command executed")
