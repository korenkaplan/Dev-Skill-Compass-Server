import os
from logic.pipelines.main import thread_pool_role_pipline_test, thread_pool_role_pipline
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from utils.functions import write_text_to_file

# Determine the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the log file
log_file_path = os.path.join(project_root, "Logs", "daily_pipeline.log.txt")


def daily_pipeline():
    try:
        # Define the time period
        period: GoogleJobsTimePeriod = GoogleJobsTimePeriod.TODAY

        # Run the main pipeline with the period time set to one day
        thread_pool_role_pipline(period)

    except Exception as e:
        # Log the error or handle it as needed
        message = f"An error occurred during the daily pipeline: {e}"
        write_text_to_file(log_file_path, 'a', message)



