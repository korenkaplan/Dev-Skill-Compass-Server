"""This is the main pipeline that runs once a week to refresh the data in the database."""
# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_server.settings')

application = get_wsgi_application()
# endregion

from usage_stats.models import TechnologiesCounts
from decorators.decorator_measure_function_time import log_runtime
from core.models import Roles, Technologies, Categories
from logic.web_scraping.google_jobs.google_jobs_scraping import GoogleJobsTimePeriod, \
    get_job_listings_google_jobs_pipeline
from logic.web_scraping.main_scrape_file import job_scrape_pipeline, configure_google_jobs_scrape_engine
from logic.text_analysis.tech_term_finder import find_tech_terms_pool_threads
from logic.data_processing.data_aggragation import data_processing_pipeline
from concurrent.futures import ThreadPoolExecutor
from usage_stats.services.technologies_counts_service import update_technologies_counts_table_in_db_pipeline
from core.services.technologies_service import get_tech_dict


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


def scrape_job_listings(role: str, time_period: GoogleJobsTimePeriod) -> list[str]:
    """Scrape job listings for a given role."""
    try:
        return job_scrape_pipeline(role, time_period)
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


def process_the_tech_words_from_analysis(jobs_sets_list: list[set[str]], role: str, tech_dict: dict) -> dict:
    """Process tech words from analysis."""
    try:
        return data_processing_pipeline(jobs_sets_list, role, tech_dict)
    except Exception as e:
        print(f"Error while processing tech words from analysis for role {role}: {e}")
        return {}


def update_the_database(role_techs_tuple: (str, dict)):
    """Update the database."""
    try:
        update_technologies_counts_table_in_db_pipeline(role_techs_tuple)
    except Exception as e:
        print(f"Error while updating the database for role {role_techs_tuple[0]}: {e}")


def single_role_pipline(role: str, tech_set: set, tech_dict: dict, time_period: GoogleJobsTimePeriod):
    """Pipeline for each role."""
    try:
        print(f'({role}) Started collecting job listings...')
        job_listings: list[str] = scrape_job_listings(role, time_period)
        print(f'({role}) Started extracting tech words from job listings...')
        tech_sets_list: list[set[str]] = extract_tech_words_from_job_listings(job_listings, tech_set)
        print(f'({role}) Started processing the extracted words...')
        role_techs_tuple: (str, dict) = process_the_tech_words_from_analysis(tech_sets_list, role, tech_dict)
        print(f'({role}) Started inserting to db...')
        update_the_database(role_techs_tuple)
        print(f'({role}) Finished pipeline successfully')
    except Exception as e:
        print(f"Error in pipeline for role {role}: {e}")


def process_pool_role_pipline():
    """Main function that creates a process for each role."""
    try:
        roles_list = get_all_roles()
        tech_set = get_all_techs_from_db()
        tech_dictionary = get_tech_dict()
        google_jobs_time_period_month = GoogleJobsTimePeriod.MONTH
        with ThreadPoolExecutor(max_workers=len(roles_list)) as executor:
            futures = [executor.submit(single_role_pipline, role, tech_set, tech_dictionary,
                                       google_jobs_time_period_month) for role in roles_list]

            # Wait for all tasks to complete
            for future in futures:
                future.result()
    except Exception as e:
        print(f"Error in main pipeline: {e}")


log_path = r"logic/web_scraping/Logs/main_pipeline_runtime.txt"


# Get the role
backend_role = Roles.objects.filter(name="Backend Developer").first()

# get the counts for the role
backend_role_counts = TechnologiesCounts.objects.filter(role_id=backend_role)

# Assuming you want to filter Technologies based on its name
programming_language_category_name = "web_frameworks"

# Get the category
programming_language_category = Categories.objects.filter(name=programming_language_category_name).first()

# Make sure the category exists before proceeding
if programming_language_category:
    # Now get the top 10 from tech counts and order by counter
    top_backend_programming_counts = backend_role_counts.all().order_by("-counter")[:20]



    for item in top_backend_programming_counts:
        print(item)
else:
    print(f"Category '{programming_language_category_name}' does not exist.")


# @log_runtime(log_path)
# def process_pool_role_pipline_test():
#     """Main function that creates a process for each role."""
#     try:
#         # roles_list = get_all_roles()
#         roles_list = ["Backend Developer", "Frontend Developer", "Full Stack Developer"]
#         tech_set = get_all_techs_from_db()
#         tech_dictionary = get_tech_dict()
#         google_jobs_time_period_month = GoogleJobsTimePeriod.MONTH
#         with ThreadPoolExecutor(max_workers=len(roles_list)) as executor:
#             futures = [executor.submit(single_role_pipline, role, tech_set, tech_dictionary,
#                                        google_jobs_time_period_month) for role in roles_list]
#
#             # Wait for all tasks to complete
#             for future in futures:
#                 future.result()
#     except Exception as e:
#         print(f"Error in main pipeline: {e}")
#
#
# process_pool_role_pipline_test()
# config = configure_google_jobs_scrape_engine('Backend Developer', GoogleJobsTimePeriod.MONTH)
# get_job_listings_google_jobs_pipeline(config)
