"""This is a test module for data_aggregation file"""
from collections import defaultdict

'''sample_data_for_'''
import pytest
from logic.data_processing.data_aggragation import (get_lists_of_jobs_and_their_role,
                                                    sum_results_of_job_listings_analysis, group_synonyms_words,
                                                    divide_words_into_categories, assign_aggregated_dict_to_role,
                                                    data_processing_pipeline)

# region Sample Data For Tests
sample_data_for_sum_results_of_job_listings_analysis: list[set[str]] = [{'python', 'django', 'restful api'},
                                                                        {'javascript', 'mongodb', 'express.js',
                                                                         'node.js'},
                                                                        {'python', 'javascript', 'mongodb'}]
sample_data_for_group_synonyms_words = defaultdict(int, {
    'python': 2,
    'django': 1,
    'restful api': 1,
    'javascript': 2,
    'mongodb': 2,
    'express.js': 1,
    'node.js': 1
})


# endregion

# region Tests
def test_sum_results_of_job_listings_analysis():
    """Test: group and sum words from all the sets"""
    expected_result: dict[str:int] = sample_data_for_group_synonyms_words

    result_dict = sum_results_of_job_listings_analysis(sample_data_for_sum_results_of_job_listings_analysis)
    # compare the lengths
    assert len(result_dict) == len(expected_result)
    # compare key values with expected result
    for k, v in result_dict:
        # compare the values of the same key
        assert v == expected_result[k]

# endregion
