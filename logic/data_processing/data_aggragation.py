"""This is a module for data aggregating and processing the results of the job listings text analysis"""
from collections import defaultdict
from logic.text_analysis.data_loookup_functions import find_first_word_in_dict
# TODO: Change the dependency on find_first_word_in_dict to a function th


def sum_results_of_job_listings_analysis(jobs_sets_list: list[set[str]]) -> dict[str:int]:
    """
    Summarizes the results of job listings analysis by counting the occurrences of each term in the provided list
    of sets.

    Args:
        jobs_sets_list (list[set[str]]): A list of sets containing terms extracted from job listings.

    Returns:
        dict[str:int]: A dictionary where keys are terms and values are the corresponding counts.
    """
    result_dict = defaultdict(int)
    # iterate over the sets of terms and add them to the result
    for term_set in jobs_sets_list:
        for term in term_set:
            if term in result_dict:
                result_dict[term] += 1
            else:
                result_dict[term] = 1
    return result_dict


def group_synonyms_words(terms_dict: dict) -> dict[str:int]:
    """
    Groups synonym words together and sums their counts.

    Args:
        terms_dict (dict): A dictionary containing terms and their counts.

    Returns:
        dict[str:int]: A dictionary where keys are grouped synonym words and values are the corresponding counts.
    """
    # create a result dictionary
    result_dict = defaultdict(int)
    # iterate over the terms_dict and check the keys
    for tech_term, count in terms_dict.items():
        # check in which group the term is in the origin data.
        result: tuple = find_first_word_in_dict(tech_term)
        # if a result is found
        if len(result) > 0:
            group_word = result[1]
            # check if the group word already exists in the dictionary and increase by count or create a new one
            if group_word in result_dict:
                result_dict[group_word] += count
            else:
                result_dict[group_word] = count

    return result_dict


def divide_words_into_categories(terms_dict: dict) -> defaultdict[str, defaultdict[str, int]]:
    """
    Divides terms into categories based on the _tech dictionary.

    Args:
        terms_dict (dict): A dictionary containing terms and their counts.

    Returns:
        defaultdict[str, defaultdict[str, int]]: A nested defaultdict where outer keys are categories and inner keys
        are terms, with corresponding counts.
    """
    result_dict = defaultdict(lambda: defaultdict(int))
    # iterate over the  words dictionary
    for tech_term, count in terms_dict.items():
        # find the category of each word in the dictionary
        result: tuple = find_first_word_in_dict(tech_term)
        # get the category
        category = result[0]
        # add the tech term and the category if not exists
        result_dict[category][tech_term] = count
    return result_dict


def assign_aggregated_dict_to_role(role: str, terms_and_technologies_dictionary: (str, dict)):
    """
    Assigns an aggregated dictionary of terms and technologies to a role.

    Args:
        role (str): The role to which the aggregated dictionary belongs.
        terms_and_technologies_dictionary (dict[str, dict[str:int]]): A dictionary containing terms and technologies
        aggregated by category.

    Returns:
        dict: A dictionary where the role is the key and the aggregated dictionary is the value.
    """
    return role, terms_and_technologies_dictionary


def data_processing_pipeline(jobs_sets_list: list[set[str]], role: str) -> (str, dict):
    """
    Runs the data processing pipeline to aggregate and categorize job listing terms and technologies.

    Args:
        jobs_sets_list (list[set[str]]): A list of sets containing terms extracted from job listings.
        role (str): The role for which the terms and technologies are being processed.

    Returns:
        dict: A dictionary containing the processed and aggregated terms and technologies categorized by role.
    """
    # Sum the results of the job listings.
    summed_jobs_sets: dict[str:int] = sum_results_of_job_listings_analysis(jobs_sets_list)

    # Group words from the same words group (e.g. postgres & postgresql)
    grouped_dict: dict[str:int] = group_synonyms_words(summed_jobs_sets)

    # divide them into categories based on the _tech dictionary
    categorized_dict = divide_words_into_categories(grouped_dict)

    # combine the role with the categorized dict
    final_dict = assign_aggregated_dict_to_role(role, categorized_dict)

    return final_dict
