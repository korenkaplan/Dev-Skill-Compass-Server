import os
import time

from logic.pipelines.main import thread_pool_role_pipline
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
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


def daily_pipeline():
    try:
        print("started daily pipeline...")
        # Define the time period
        period: GoogleJobsTimePeriod = GoogleJobsTimePeriod.TODAY
        period: GoogleJobsTimePeriod = GoogleJobsTimePeriod.MONTH

        # Run the main pipeline with the period time set to one day
        thread_pool_role_pipline(period)

    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the daily pipeline: {e}"
        print(message)


def daily_test():
    print("started daily test...")

