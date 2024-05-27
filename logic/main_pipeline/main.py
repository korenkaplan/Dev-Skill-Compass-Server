"""This is the main pipeline that runs once a week to refresh the data in the database."""

from core.models import Roles, Technologies
from logic.web_scraping.main_scrape_file import job_scrape_pipeline
import uuid
from logic.text_analysis.tech_term_finder import find_tech_terms_pool_threads
from logic.data_processing.data_aggragation import data_processing_pipeline
from concurrent.futures import ThreadPoolExecutor
from usage_stats.services.technologies_counts_service import update_technologies_counts_table_in_db_pipeline


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
        return {tech.name for tech in Technologies.objects.all()}
    except Exception as e:
        print(f"Error while querying technologies: {e}")
        return set()


def scrape_job_listings(role: str) -> list[str]:
    """Scrape job listings for a given role."""
    try:
        return job_scrape_pipeline(role)
    except Exception as e:
        print(f"Error while scraping job listings for role {role}: {e}")
        return []


def extract_tech_words_from_job_listings(listings_list: list[str], tech_set: set) -> list[set]:
    """Extract tech words from job listings."""
    try:
        return find_tech_terms_pool_threads(listings_list, tech_set)
    except Exception as e:
        print(f"Error while extracting tech words from job listings: {e}")
        return []


def process_the_tech_words_from_analysis(jobs_sets_list: list[set[str]], role: str) -> dict:
    """Process tech words from analysis."""
    try:
        return data_processing_pipeline(jobs_sets_list, role)
    except Exception as e:
        print(f"Error while processing tech words from analysis for role {role}: {e}")
        return {}


def update_the_database(role_techs_tuple: (str, dict)):
    """Update the database."""
    try:
        update_technologies_counts_table_in_db_pipeline(role_techs_tuple)
    except Exception as e:
        print(f"Error while updating the database for role {role_techs_tuple[0]}: {e}")


def single_role_pipline(role: str, tech_set: set):
    """Pipeline for each role."""
    try:
        job_listings: list[str] = scrape_job_listings(role)
        tech_sets_list: list[set[str]] = extract_tech_words_from_job_listings(job_listings, tech_set)
        role_techs_tuple: (str, dict) = process_the_tech_words_from_analysis(tech_sets_list, role)
        update_the_database(role_techs_tuple)
    except Exception as e:
        print(f"Error in pipeline for role {role}: {e}")


def process_pool_role_pipline():
    """Main function that creates a process for each role."""
    try:
        roles_list = get_all_roles()
        tech_set = get_all_techs_from_db()

        with ThreadPoolExecutor(max_workers=len(roles_list)) as executor:
            futures = [executor.submit(single_role_pipline, role, tech_set) for role in roles_list]

            # Wait for all tasks to complete
            for future in futures:
                future.result()
    except Exception as e:
        print(f"Error in main pipeline: {e}")


# Example usage
process_pool_role_pipline()
