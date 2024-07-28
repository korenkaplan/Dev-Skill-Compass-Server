"""This is the main pipeline that runs once a week to refresh the data in the database."""
from core.models import Roles, Synonyms
from core.services.role_listings_count_services import update_job_listings_count_table
from logic.web_scraping.main_scrape_file import (
    job_scrape_pipeline,
)
from logic.text_analysis.tech_term_finder import find_tech_terms_pool_threads
from logic.data_processing.data_aggragation import data_processing_pipeline
from concurrent.futures import ThreadPoolExecutor
from usage_stats.services.technologies_counts_service import (
    update_monthly_counts_table_and_aggregated_table_in_db_pipeline,
)
from core.services.technologies_service import get_tech_dict
from utils.enums import LinkedinTimePeriod
from utils.mail_module.email_module_functions import send_recap_email_prepared
from utils.settings import MAX_NUMBER_OF_WORKERS, MAX_NUMBER_OF_RETRIES_SCARPING
from concurrent.futures import as_completed
from memory_profiler import profile


def get_all_roles() -> list[str]:
    """Query all roles from the database."""
    try:
        return [role.name for role in Roles.objects.all()]
    except Exception as e:
        print(f"Error while querying roles: {e}")
        return []


def get_all_techs_from_db() -> set:
    """Query all technologies from the database."""
    try:
        return {synonym.name for synonym in Synonyms.objects.all()}
    except Exception as e:
        print(f"Error while querying technologies: {e}")
        return set()


def scrape_job_listings(role: str, linkedin_time_period: LinkedinTimePeriod) -> list[str]:
    """Scrape job listings for a given role."""
    result = []
    attempts = 1
    while len(result) == 0 and attempts <= MAX_NUMBER_OF_RETRIES_SCARPING:
        try:
            result = job_scrape_pipeline(role, linkedin_time_period)

        except Exception as e:
            print(f"Error while scraping job listings for role {role} attempt number {attempts}: {e}")
        finally:
            attempts += 1

    return result


def extract_tech_words_from_job_listings(
        listings_list: list[str], tech_set: set
) -> list[set]:
    """Extract tech words from job listings."""
    try:
        return find_tech_terms_pool_threads(listings_list, tech_set)
    except Exception as e:
        print(f"Error while extracting tech words from job listings: {e}")
        return []


def process_the_tech_words_from_analysis(
        jobs_sets_list: list[set[str]], role: str, tech_dict: dict
) -> dict:
    """Process tech words from analysis."""
    try:
        return data_processing_pipeline(jobs_sets_list, role, tech_dict)
    except Exception as e:
        print(f"Error while processing tech words from analysis for role {role}: {e}")
        return {}


def update_the_database(role_techs_tuple: (str, dict)):
    """Update the database."""
    try:
        update_monthly_counts_table_and_aggregated_table_in_db_pipeline(role_techs_tuple)
    except Exception as e:
        print(f"Error while updating the database for role {role_techs_tuple[0]}: {e}")


def update_or_create_role_jobs_count_table(job_listings: list, role: str):
    try:
        amount = len(job_listings)
        update_job_listings_count_table(amount, role)
    except Exception as e:
        print(f"Error while updating the role and jobs count table: {e}")


def collect_results(futures: list[tuple[str, int]]) -> str:
    """Collect results from futures and return as a single string."""
    total_count = 0
    final_message = []
    try:
        for result in futures:
            final_message.append(f"{result[0]}: {result[1]}")
            total_count += result[1]
        final_message.append("-------------------------------")
        final_message.append(f"Total: {total_count}")
    except Exception as e:
        print(f"Error collecting results: {e}")
    return '\n'.join(final_message)


def single_role_pipline(
        role: str, tech_set: set, tech_dict: dict, linkedin_time_period: LinkedinTimePeriod):
    """Pipeline for each role."""
    try:
        print(f"({role}) Started collecting job listings...")
        job_listings: list[str] = scrape_job_listings(role, linkedin_time_period)
        print(f"({role}) Started extracting tech words from job listings...")
        tech_sets_list: list[set[str]] = extract_tech_words_from_job_listings(
            job_listings, tech_set
        )
        print(f"({role}) Started processing the extracted words...")
        role_techs_tuple: (str, dict) = process_the_tech_words_from_analysis(
            tech_sets_list, role, tech_dict
        )
        print(f"({role}) Started inserting to db...")
        update_the_database(role_techs_tuple)

        print(f"({role}) Started updating jobs count table...")
        update_or_create_role_jobs_count_table(job_listings, role)

        print(f"({role}) Finished pipeline successfully")
        return role.title(), len(job_listings)
    except Exception as e:
        print(f"Error in pipeline for role {role}: {e}")


@profile
def thread_pool_role_pipline(linkedin_period: LinkedinTimePeriod):
    """Main function that creates a process for each role."""
    try:
        roles_list = get_all_roles()
        tech_set = get_all_techs_from_db()
        tech_dictionary = get_tech_dict()
        linkedin_time_period = linkedin_period
        with ThreadPoolExecutor(max_workers=MAX_NUMBER_OF_WORKERS) as executor:
            futures = [
                executor.submit(
                    single_role_pipline,
                    role,
                    tech_set,
                    tech_dictionary,
                    linkedin_time_period
                )
                for role in roles_list
            ]

            # Wait for all tasks to complete
            for future in futures:
                future.result()

            # create the string of the email:
            result = [future.result() for future in as_completed(futures)]
            email_text = collect_results(result)

            # Send the email summarizing the scan session
            send_recap_email_prepared(email_text, 'Google Jobs')
    except Exception as e:
        print(f"Error in main pipeline: {e}")


def thread_pool_role_pipline_test(linkedin_period: LinkedinTimePeriod, roles):
    """Main function that creates a process for each role."""
    try:
        roles_list = roles
        tech_set = get_all_techs_from_db()
        tech_dictionary = get_tech_dict()
        linkedin_time_period = linkedin_period
        with ThreadPoolExecutor(max_workers=MAX_NUMBER_OF_WORKERS) as executor:
            futures = [
                executor.submit(
                    single_role_pipline,
                    role,
                    tech_set,
                    tech_dictionary,
                    linkedin_time_period
                )
                for role in roles_list
            ]

            # Wait for all tasks to complete
            for future in futures:
                future.result()

            # create the string of the email:
            result = [future.result() for future in as_completed(futures)]
            email_text = collect_results(result)

            # Send the email summarizing the scan session
            send_recap_email_prepared(email_text, 'Google Jobs')
    except Exception as e:
        print(f"Error in main pipeline: {e}")
