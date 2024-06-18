from django.core.cache import cache
from django.core.management.base import BaseCommand
from logic.pipelines.main import (
    thread_pool_role_pipline
)
from decorators.decorator_measure_function_time import measure_function_time
from utils.enums import GoogleJobsTimePeriod, LinkedinTimePeriod
from utils.functions import retry_function
from utils.mail_module.email_module_functions import send_scan_recap_email


class Command(BaseCommand):
    help = "Run the main pipeline"

    @measure_function_time
    def handle(self, *args, **options):
        # Call your initialization function here
        retry_function(test_send_email, role_name='test_send_email')
        retry_function(daily_test, role_name='daily_test')
        # process_pool_role_pipline()
        self.stdout.write("test_send_email command executed")


def test_send_email():
    recipient_email = 'korenkaplan96@gmail.com'
    website_name = 'Google Jobs'
    date_and_time = '12321'
    text = 'this is a test email'
    send_scan_recap_email(recipient_email, website_name, date_and_time, text)


def daily_test():
    print("started daily test...")
