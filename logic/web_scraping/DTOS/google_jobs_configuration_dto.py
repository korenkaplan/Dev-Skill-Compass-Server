from pydantic import BaseModel
from logic.web_scraping.google_jobs.google_jobs_scraping import GoogleJobsTimePeriod


class GoogleJobsConfigDto(BaseModel):
    search_value: str
    time_period: GoogleJobsTimePeriod
    show_full_description_button_xpath: str
    expandable_job_description_text_xpath: str
    not_expandable_job_description_text_xpath: str
    max_interval_attempts: int
    sleep_time_between_attempt_in_seconds: int
    wait_driver_timeout: int
    log_file_path: str
