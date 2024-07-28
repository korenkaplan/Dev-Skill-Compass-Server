""" this is the main entry point for scraping module"""
import os
from dotenv import load_dotenv

from logic.web_scraping.linkedin.build_url import build_url
from logic.web_scraping.linkedin.linkedin_scraping_functions import get_listings_from_linkedin
from utils.enums import LinkedinTimePeriod
from utils.functions import write_text_to_file

load_dotenv()


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


def write_run_recap_to_file(linkedin_amount, role, log_file_path):
    log_text = f"""
        ({role}) -> Total Jobs Scraped from linkedIn: {linkedin_amount}
    """
    write_text_to_file(log_file_path, 'a', log_text)


def job_scrape_pipeline(role: str,
                        linkedin_time_period: LinkedinTimePeriod) -> list[str]:
    # Determine the project root directory
    scraping_folder_path = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the log file
    log_file_path = os.path.join(scraping_folder_path, "Logs", "scrape_run_recap.log.txt")

    # All jobs listings from all sites
    job_listings_list: list[str] = []
    print(f"({role}) -> Started LinkedIn Scraper")

    # get the listings from Google jobs
    linkedin_jobs_listings = linkedin_scraping_entry_point(role, linkedin_time_period)

    # combine the lists together
    job_listings_list.extend(linkedin_jobs_listings)
    print(f"({role}) -> Finished LinkedIn Scraper")

    amount_of_listings_from_linkedin = len(job_listings_list)

    write_run_recap_to_file(amount_of_listings_from_linkedin, role, log_file_path)
    # add more lists from other sites...

    # return final result
    return job_listings_list
