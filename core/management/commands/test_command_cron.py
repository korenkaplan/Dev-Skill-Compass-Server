from django.core.management.base import BaseCommand
from decorators.decorator_measure_function_time import measure_function_time


class Command(BaseCommand):
    help = "Run the test cron"

    @measure_function_time
    def handle(self, *args, **options):
        # Call your initialization function here
        self.stdout.write(self.style.SUCCESS("Run the test cron command executed"))
