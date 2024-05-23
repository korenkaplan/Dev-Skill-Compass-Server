"""This is a module for data aggregating and processing the results of the job listings text analysis"""
from collections import defaultdict


# Sum the results of the job listings.
def sum_results_of_job_listings_analysis(jobs_sets_list: list[set[str]]) -> dict:
    pass


# Group Synonyms words together example: postgres and postgresql or gcp and google cloud,
# decide the representing word for the group.
def group_synonyms_words(terms_dict: dict) -> dict:
    pass


# divide them into categories based on the _tech dictionary from text_analysis.data.skills_data.
def divide_words_into_categories(terms_dict: defaultdict) -> dict:
    pass


# Create a dictionary representing the roles and technologies by category example below.
# region Desired data structure example
"""roles = {
    "backend_developer": {
        "programming_languages": {
            "python": 10,
            "java": 8,
        },
        "databases": {
            "postgresql": 10,
            "mysql": 11,
        },
    "frontend_developer": {
        "programming_languages": {
            "Javascript": 10,
            "Typescript": 8,
        },
        "web_frameworks": {
            "react": 10,
            "angular": 11,
        }
    }
}"""


# endregion
def assign_aggregated_dict_to_role(role: str, terms_and_technologies: dict) -> dict:
    pass


# The main entry point for the pipeline
def data_processing_pipeline(jobs_sets_list: list[set[str]], role: str) -> dict:
    pass
