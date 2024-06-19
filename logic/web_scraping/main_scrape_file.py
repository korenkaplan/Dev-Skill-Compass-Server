""" this is the main entry point for scraping module"""

from utils.enums import GoogleJobsTimePeriod
from logic.web_scraping.google_jobs.DTO.google_jobs_configuration_dto import (
    GoogleJobsConfigDto,
)
from logic.web_scraping.google_jobs.google_jobs_scraping import (
    get_job_listings_google_jobs_pipeline,
)

import os
from dotenv import load_dotenv

from logic.web_scraping.linkedin.build_url import build_url
from logic.web_scraping.linkedin.linkedin_scraping_functions import get_listings_from_linkedin
from utils.enums import LinkedinTimePeriod
from utils.functions import write_text_to_file
from utils.settings import NOT_EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS, \
    SHOW_FULL_DESCRIPTION_BUTTON_XPATH_GOOGLE_JOBS, EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS

load_dotenv()


# region Google Jobs Configuration
def configure_google_jobs_scrape_engine(
    role: str, time_period: GoogleJobsTimePeriod
) -> GoogleJobsConfigDto:
    # Determine the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the log file
    scrape_google_log_file_path = os.path.join(project_root, "Logs", "google",
                                               f"{role}.txt")
    google_jobs_configuration = GoogleJobsConfigDto(
        role=role,
        time_period=time_period,
        show_full_description_button_xpath=SHOW_FULL_DESCRIPTION_BUTTON_XPATH_GOOGLE_JOBS,
        expandable_job_description_text_xpath=EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS,
        not_expandable_job_description_text_xpath=NOT_EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS,
        max_interval_attempts=10,
        sleep_time_between_attempt_in_seconds=30,
        wait_driver_timeout=3,
        log_file_path=f"{scrape_google_log_file_path}",
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
    # Determine the project root directory
    scraping_folder_path = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the log file
    log_file_path = os.path.join(scraping_folder_path, "Logs", "linkedin", f"{role}.txt")
    # Format the url
    formatted_url = build_url(role, linkedin_time_period)

    # Scrape the full descriptions of the job listings
    job_listings_descriptions_list = get_listings_from_linkedin(formatted_url, role, log_file_path)

    # Check if the job listings fetch happened successfully
    if job_listings_descriptions_list is None:
        print("Could not get the job listings")
        return []

    return job_listings_descriptions_list
# endregion


def write_run_recap_to_file(google_amount, linkedin_amount, role, log_file_path):
    log_text = f"""
        ({role}) -> Total Jobs Scraped from Google Jobs: {google_amount}
        ({role}) -> Total Jobs Scraped from linkedIn: {linkedin_amount}
    """
    write_text_to_file(log_file_path, 'a', log_text)


def job_scrape_pipeline(role: str, google_time_period: GoogleJobsTimePeriod,
                        linkedin_time_period: LinkedinTimePeriod) -> list[str]:
    # Determine the project root directory
    scraping_folder_path = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the log file
    log_file_path = os.path.join(scraping_folder_path, "Logs", "scrape_run_recap.log.txt")

    # All jobs listings from all sites
    job_listings_list: list[str] = []

    # get the listings from Google jobs
    google_jobs_listings = google_jobs_scraping_pipeline(role, google_time_period)

    # combine the lists together
    job_listings_list.extend(google_jobs_listings)

    amount_of_listings_from_google_job = len(job_listings_list)

    # get the listings from Google jobs
    linkedin_jobs_listings = linkedin_scraping_entry_point(role, linkedin_time_period)

    # combine the lists together
    job_listings_list.extend(linkedin_jobs_listings)
    amount_of_listings_from_linkedin = len(job_listings_list) - amount_of_listings_from_google_job

    write_run_recap_to_file(amount_of_listings_from_google_job,
                            amount_of_listings_from_linkedin, role, log_file_path)
    # add more lists from other sites...

    # return final result
    return job_listings_list
