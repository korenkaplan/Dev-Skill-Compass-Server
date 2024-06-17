import os
from logic.pipelines.main import thread_pool_role_pipline
from utils.enums import LinkedinTimePeriod, GoogleJobsTimePeriod
from django.core.cache import cache
from utils.mail_module.email_module_functions import send_scan_recap_email

# Determine the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the log file
log_file_path = os.path.join(project_root, "Logs", "daily_pipeline.log.txt")


def test_send_email():
    recipient_email = 'korenkaplan96@gmail.com'
    website_name = 'Google Jobs'
    date_and_time='12321'
    text = 'this is a test email'
    send_scan_recap_email(recipient_email, website_name, date_and_time, text)





def daily_test():
    print("started daily test...")

