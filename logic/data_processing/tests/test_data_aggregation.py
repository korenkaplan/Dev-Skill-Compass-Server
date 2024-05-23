"""This is a test module for data_aggregation file"""

import pytest
from collections import defaultdict
from logic.data_processing.data_aggragation import (sum_results_of_job_listings_analysis, group_synonyms_words,
                                                    divide_words_into_categories, assign_aggregated_dict_to_role,
                                                    data_processing_pipeline)
from logic.text_analysis.data.data import get_tech_dict

# region Sample Data For Tests
tech_dict = get_tech_dict()
sample_data_for_sum_results_of_job_listings_analysis: list[set[str]] = [{'python', 'django', 'restful api'},
                                                                        {'javascript', 'mongodb', 'express.js',
                                                                         'node.js'},
                                                                        {'python', 'javascript', 'mongodb'}]
sample_data_for_group_synonyms_words = defaultdict(int, {
    'javascript': 2,
    'js': 1,
    'restful api': 1,
    'typescript': 2,
    'ts': 2,
    'csharp': 1,
    'c-sharp': 3
})
sample_data_for_divide_words_into_categories = defaultdict(int,
                                                           {'javascript': 3, 'typescript': 4, 'c#': 4, 'restful': 1})

sample_data_for_assign_aggregated_dict_to_role = {'programming_languages': {'javascript': 3, 'typescript': 4, 'c#': 4},
                                                  'data_exchange_apis_and_tools': {'restful': 1}}
role_name_for_assign_aggregated_dict_to_role = 'backend developer'

sample_data_for_data_processing_pipeline = sample_data_for_sum_results_of_job_listings_analysis


# endregion
# region Tests
def test_data_processing_pipeline():
    """Test the whole processing pipeline is working"""
    sample_data = [{'nodejs', 'typescript', 'postgres'}, {'python', 'sqlite', 'django', 'postgresql'},
                   {'java', 'spring-boot', 'redis', 'ts'}]

    expected_result = {
        "backend developer": {
            "databases": {
                "postgresql": 2,
                "sqlite": 1,
                "redis": 1
            },
            "web_frameworks": {
                "node.js": 1,
                "django": 1,
                "spring boot": 1
            },
            "programming_languages": {
                "typescript": 2,
                "python": 1,
                "java": 1
            }
        }
    }
    res = data_processing_pipeline(sample_data,
                                   role_name_for_assign_aggregated_dict_to_role)

    # compare the results
    for role, techs in res.items():
        for category, tech_dicts in techs.items():
            for tech_name, count in tech_dicts.items():
                assert res[role][category][tech_name] == expected_result[role][category][tech_name]


def test_assign_aggregated_dict_to_role():
    """Test creating an object from the role and the aggregated data"""
    expected_result = {role_name_for_assign_aggregated_dict_to_role: sample_data_for_assign_aggregated_dict_to_role}

    res = assign_aggregated_dict_to_role(role_name_for_assign_aggregated_dict_to_role,
                                         sample_data_for_assign_aggregated_dict_to_role)
    # compare lengths
    assert compare_lengths([res, expected_result])
    # compare dictionaries
    assert res == expected_result


def test_divide_words_into_categories():
    """Test: divide the grouped words into their origin categories"""
    expected_results = {'programming_languages': {'javascript': 3, 'typescript': 4, 'c#': 4},
                        'data_exchange_apis_and_tools': {'restful': 1}}
    expected_false_results = {'programming_languages': {'javascript': 3, 'typescript': 4, 'c#': 4, 'java': 1},
                              'data_exchange_apis_and_tools': {'restful': 1}}
    res = divide_words_into_categories(sample_data_for_divide_words_into_categories)

    assert res == expected_results
    assert res != expected_false_results


def test_group_synonyms_words():
    """Test: should group synonyms words from the same group together and sum their counts"""
    expected_results = {'javascript': 3, 'typescript': 4, 'c#': 4, 'restful': 1}
    res = group_synonyms_words(sample_data_for_group_synonyms_words)

    # compare the lengths of the dictionaries
    assert len(res) == len(expected_results)
    # compare the values of the keys
    for key, value in res.items():
        assert value == expected_results[key]


def test_sum_results_of_job_listings_analysis():
    """Test: group and sum words from all the sets"""
    expected_result: dict[str:int] = {'python': 2, 'django': 1, 'restful api': 1, 'javascript': 2, 'mongodb': 2,
                                      'express.js': 1, 'node.js': 1}

    result_dict = sum_results_of_job_listings_analysis(sample_data_for_sum_results_of_job_listings_analysis)
    # compare the lengths
    assert len(result_dict) == len(expected_result)
    # compare key values with expected result
    for k, v in result_dict.items():
        # compare the values of the same key
        assert v == expected_result[k]


# endregion
# region Helping functions
def compare_lengths(data_structures: list):
    """A function that assert lengths of data structures"""
    length_to_compare = len(data_structures[0])
    if len(data_structures) == 1:
        return True
    for item in data_structures[1:]:
        if len(item) != length_to_compare:
            return False
    return True


def test_compare_lengths_():
    list1 = {'test_length': 1, 'test_length2': 2}
    list2 = {'test_length': 4, 'test_length2': 3}
    list3 = {'test_length': 4, 'test_length2': 3, 'test_length3': 3}

    assert compare_lengths([list1, list2]) is True

    assert compare_lengths([list1, list3]) is False


# endregion


if __name__ == '__main__':
    #  pytest test_data_aggregation.py "test_sum_results_of_job_listings_analysis"
    pytest.main()
