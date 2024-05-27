"""This is a module for data aggregating and processing the results of the job listings text analysis"""
from collections import defaultdict
from logic.text_analysis.data_loookup_functions import find_first_word_in_dict


def sum_results_of_job_listings_analysis(jobs_sets_list: list[set[str]]) -> dict[str, int]:
    """
    Summarizes the results of job listings analysis by counting the occurrences of each term in the provided list
    of sets.

    Args:
        jobs_sets_list (list[set[str]]): A list of sets containing terms extracted from job listings.

    Returns:
        dict[str, int]: A dictionary where keys are terms and values are the corresponding counts.
    """
    result_dict = defaultdict(int)
    try:
        # iterate over the sets of terms and add them to the result
        for term_set in jobs_sets_list:
            for term in term_set:
                result_dict[term] += 1
    except Exception as e:
        print(f"Error during summing results of job listings analysis: {e}")
    return result_dict


def group_synonyms_words(terms_dict: dict, tech_dict: dict) -> dict[str, int]:
    """
    Groups synonym words together and sums their counts.

    Args:
        terms_dict (dict): A dictionary containing terms and their counts.
        tech_dict: THE TECHNOLOGY DICTIONARY FROM DB TO THE
    Returns:
        dict[str, int]: A dictionary where keys are grouped synonym words and values are the corresponding counts.
    """
    result_dict = defaultdict(int)

    for tech_term, count in terms_dict.items():
        try:
            result = find_first_word_in_dict(tech_term, tech_dict)
        except Exception as e:
            print(f"Error finding first word in dict for term '{tech_term}': {e}")
            continue

        if result:
            group_word = result[1]
            result_dict[group_word] += count
    return result_dict


def divide_words_into_categories(terms_dict: dict, tech_dict: dict) -> defaultdict[str, defaultdict[str, int]]:
    """
    Divides terms into categories based on the _tech dictionary.

    Args:
         terms_dict (dict): A dictionary containing terms and their counts.
         tech_dict: tech dictionary form db

    Returns:
        defaultdict[str, defaultdict[str, int]]: A nested defaultdict where outer keys are categories and inner keys
        are terms, with corresponding counts.
    """
    result_dict = defaultdict(lambda: defaultdict(int))
    try:
        for term, count in terms_dict.items():
            try:
                result = find_first_word_in_dict(term, tech_dict)
                category = result[0]
                result_dict[category][term] = count
            except Exception as e:
                print(f"Error categorizing term '{term}': {e}")
    except Exception as e:
        print(f"Error during dividing words into categories: {e}")
    return result_dict


def assign_aggregated_dict_to_role(role: str, terms_and_technologies_dictionary: (str, dict)) -> (str, dict):
    """
    Assigns an aggregated dictionary of terms and technologies to a role.

    Args:
        role (str): The role to which the aggregated dictionary belongs.
        terms_and_technologies_dictionary (dict[str, dict[str:int]]): A dictionary containing terms and technologies
        aggregated by category.

    Returns:
        dict: A dictionary where the role is the key and the aggregated dictionary is the value.
    """
    try:
        return role, terms_and_technologies_dictionary
    except Exception as e:
        print(f"Error assigning aggregated dictionary to role '{role}': {e}")
        return role, {}


def data_processing_pipeline(jobs_sets_list: list[set[str]], role: str, tech_dictionary: dict) -> (str, dict):
    """
    Runs the data processing pipeline to aggregate and categorize job listing terms and technologies.

    Args:
        jobs_sets_list (list[set[str]]): A list of sets containing terms extracted from job listings.
        role (str): The role for which the terms and technologies are being processed.
        tech_dictionary (dict): A dictionary representing the technologies from db


    Returns:
        dict: A dictionary containing the processed and aggregated terms and technologies categorized by role.
    """
    try:
        summed_jobs_sets = sum_results_of_job_listings_analysis(jobs_sets_list)
    except Exception as e:
        print(f"Error during summing job listings: {e}")
        return role, {}

    try:
        grouped_dict = group_synonyms_words(summed_jobs_sets, tech_dictionary)
    except Exception as e:
        print(f"Error during grouping synonyms: {e}")
        return role, {}

    try:
        categorized_dict = divide_words_into_categories(grouped_dict, tech_dictionary)
    except Exception as e:
        print(f"Error during dividing words into categories: {e}")
        return role, {}

    try:
        final_dict = assign_aggregated_dict_to_role(role, categorized_dict)
    except Exception as e:
        print(f"Error during assigning aggregated dict to role: {e}")
        return role, {}

    return final_dict
