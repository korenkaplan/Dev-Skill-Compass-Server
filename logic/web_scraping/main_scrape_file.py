""" this is the main entry point for scraping module"""

from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from logic.web_scraping.google_jobs.DTO.google_jobs_configuration_dto import (
    GoogleJobsConfigDto,
)
from logic.web_scraping.google_jobs.google_jobs_scraping import (
    get_job_listings_google_jobs_pipeline,
)

import os
from dotenv import load_dotenv

load_dotenv()


# region Google Jobs Configuration
def configure_google_jobs_scrape_engine(
    role: str, time_period: GoogleJobsTimePeriod
) -> GoogleJobsConfigDto:
    google_jobs_configuration = GoogleJobsConfigDto(
        role=role,
        time_period=time_period,
        show_full_description_button_xpath=os.environ.get(
            "SHOW_FULL_DESCRIPTION_BUTTON_XPATH_GOOGLE_JOBS"
        ),
        expandable_job_description_text_xpath=os.environ.get(
            "EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS"
        ),
        not_expandable_job_description_text_xpath=os.environ.get(
            "NOT_EXPANDABLE_JOB_DESCRIPTION" "_TEXT_XPATH_GOOGLE_JOBS"
        ),
        max_interval_attempts=10,
        sleep_time_between_attempt_in_seconds=30,
        wait_driver_timeout=3,
        log_file_path=f"{os.environ.get('SCRAPE_GOOGLE_LOG_FILE_PATH')}_{role.replace(' ', '_')}.txt",
    )
    return google_jobs_configuration


def google_jobs_scraping_pipeline(
    role: str, time_period: GoogleJobsTimePeriod
) -> list[str]:
    # configure google jobs params
    google_jobs_config = configure_google_jobs_scrape_engine(role, time_period)

    # execute the pipeline
    job_listings: list[str] = get_job_listings_google_jobs_pipeline(google_jobs_config)

    # return the results
    return job_listings


# endregion


def job_scrape_pipeline(role: str, time_period: GoogleJobsTimePeriod) -> list[str]:
    # All jobs listings from all sites
    job_listings_list: list[str] = []

    # get the listings from Google jobs
    google_jobs_listings = google_jobs_scraping_pipeline(role, time_period)

    # add more lists from other sites...

    # combine the lists together
    job_listings_list.extend(google_jobs_listings)

    # return final result
    return job_listings_list
