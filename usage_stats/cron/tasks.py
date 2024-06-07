# run the daily scrape pipeline
from logic.pipelines.main import thread_pool_role_pipline
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from celery import shared_task

def daily_scrape():
    try:
        thread_pool_role_pipline(GoogleJobsTimePeriod.TODAY)
        print("Daily scrape executed successfully")
    except Exception as e:
        print(f"Failed daily scrape: {e}")