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

from logic.web_scraping.linkedin.DTO.linkedin_dtos import LinkedInScrapingDto
from logic.web_scraping.linkedin.build_url import build_url
from logic.web_scraping.linkedin.linkedin_scraping_functions import get_listings_from_linkedin
from utils.enums import LinkedinTimePeriod

load_dotenv()


# region Google Jobs Configuration
def configure_google_jobs_scrape_engine(
    role: str, time_period: GoogleJobsTimePeriod
) -> GoogleJobsConfigDto:
    # Determine the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the log file
    scrape_google_log_file_path = os.path.join(project_root, "Logs", "web_scrape_main_run_log")
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
        log_file_path=f"{scrape_google_log_file_path}_{role.replace(' ', '_')}.txt",
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

# region LinkedIn Jobs Configuration
def linkedin_scraping_entry_point(role: str, linkedin_time_period: LinkedinTimePeriod):
    # Format the url
    formatted_url = build_url(role, linkedin_time_period)

    # Scrape the full descriptions of the job listings
    job_listings_descriptions_list = get_listings_from_linkedin(formatted_url, role)

    # Check if the job listings fetch happened successfully
    if job_listings_descriptions_list is None:
        print("Could not get the job listings")
        return []

    return job_listings_descriptions_list
# endregion


def job_scrape_pipeline(role: str, google_time_period: GoogleJobsTimePeriod, linkedin_time_period: LinkedinTimePeriod) -> list[str]:
    # All jobs listings from all sites
    job_listings_list: list[str] = []

    print("Starting Scraping Jobs From Google Jobs...")
    # get the listings from Google jobs
    google_jobs_listings = google_jobs_scraping_pipeline(role, google_time_period)

    # combine the lists together
    job_listings_list.extend(google_jobs_listings)
    print("Finished Scraping Jobs From Google Jobs...")
    print("Starting Scraping Jobs From LinkedIn...")

    # get the listings from Google jobs
    linkedin_jobs_listings = linkedin_scraping_entry_point(role, linkedin_time_period)

    # combine the lists together
    job_listings_list.extend(linkedin_jobs_listings)
    print("Finished Scraping Jobs From LinkedIn...")

    # add more lists from other sites...

    # return final result
    return job_listings_list
