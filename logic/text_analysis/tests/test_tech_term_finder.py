"""Test Module for tech_term_finder module"""
import time
import pytest
from logic.text_analysis.tech_term_finder import (remove_subsets, find_phrases, preprocess_text,
                                                  tokenize_text, tokenize_text_with_slash, find_tech_terms,
                                                  find_tech_terms_pool_threads)
from logic.text_analysis.data.skills_data import get_tech_set
#  Sample data for tests
sample_text = """"
this is a test job listing for testing purposes here are some technical terms and technologies.
Python, SQL, C#, Typescript, DOCKER, java, NodeJs
"""
sample_tech_set = ('python', 'sql', 'c#', 'typescript', 'docker', 'java', 'nodejs')
tokenized_sample_text = [
    "we", "are", "looking", "for", "someone", "experienced", "with", "ci/cd", "pipelines",
    "cloud", "computing", "and", "machine", "learning", "knowledge", "of", "ux", "ui", "design", "is", "a", "plus",
    'python', 'sql', 'c#', 'typescript', 'docker', 'java', 'nodejs'
]
sample_data_for_test_remove_subset = ['microsoft sql server', 'github actions', 'github', 'sql server']
sample_data_for_test_preprocess_text = 'HeLLo WoR!@$ld'
sample_data_for_test_tokenize_text = 'Python, SQL, C#,$,ci/cd, Typescript, DOCKER, java, NodeJs'
sample_data_developer_job_listings = [
    "Backend Engineer (Python/Django): Build and maintain scalable web applications using Python and Django framework. (RESTful API, Databases)",
    "Node.js Developer (Social Media): Develop real-time features and backend services for a high-traffic social media platform. (JavaScript, Express.js, MongoDB)",
    "Java Backend Developer (FinTech): Create secure and reliable backend systems for financial transactions. (Spring Boot, Java EE, Microservices)",
    "Go Developer (Cloud Infrastructure): Develop and maintain backend services for a cloud platform using Go. (Concurrency, Postgresql)",
    "DevOps Engineer (E-commerce): Automate infrastructure provisioning and integrate development and deployment processes. (Linux, K8's, Docker)",
    "API Developer (Healthcare): Develop secure and well-documented APIs for healthcare data exchange. (RESTful APIs, OAuth, Security)",
    "Backend Developer (Machine Learning): Build backend infrastructure to support machine learning models and data pipelines. (Python, TensorFlow, Cloud Storage)",
    "Software Engineer (Embedded Systems): Develop low-level software for interacting with hardware components. (C/C++, Assembly)",
    "Front-End Developer (React/JS): Build interactive and user-friendly web interfaces using React and JavaScript. (HTML, CSS, UI/UX Design)",
    "Angular Developer (E-commerce): Develop single-page applications for an e-commerce platform using Angular. (TypeScript, RxJS)",
    "UI/UX Designer & Front-End Developer (Mobile App): Design and develop user interfaces for a mobile application. (React Native/Flutter, UI/UX Best Practices)",
    "Front-End Developer (VR/AR): Develop interactive front-end experiences for virtual and augmented reality platforms. (WebGL, Three.js)",
    "Front-End Developer (SSR): Build server-side rendered web applications for improved SEO and performance. (Next.js, Nuxt.js)",
  ]
max_time_for_handling_multiple_listings_in_seconds = 10

# Tests


def test_remove_subset():
    """Test removing a subset of a phrase"""
    expected_result = ['microsoft sql server', 'github actions']
    result = remove_subsets(sample_data_for_test_remove_subset)

    # Check length is 2
    assert len(result) == 2

    # Check that result contains the expected result
    assert expected_result[0] in result and expected_result[1] in result


def test_preprocess_text():
    """Test preprocessing a string by  converting it to lowercase and removing special characters (# / ),
    numbers, and punctuation. """
    expected_result = 'hello world'
    assert preprocess_text(sample_data_for_test_preprocess_text) == expected_result


def test_tokenize_text():
    """Test tokenizing a string into separate words"""
    expected_result = ['Python', 'SQL', 'C#', 'ci', 'cd', 'Typescript', 'DOCKER', 'java', 'NodeJs']
    assert tokenize_text(sample_data_for_test_tokenize_text) == expected_result


def test_find_phrases():
    """Test find_phrases check that """
    expected_result = ['python', 'sql', 'c#', 'typescript', 'docker', 'java', 'nodejs']
    assert find_phrases(tokenized_sample_text, sample_tech_set) == expected_result


def test_find_tech_terms():
    """"Test find_tech_terms recieves a text job listing and returns the list of tech skills"""
    expected_result = ['python', 'sql', 'c#', 'typescript', 'docker', 'java', 'nodejs']
    result = find_tech_terms(sample_text, sample_tech_set)
    # compare the lengths of the result and the expected result
    assert len(result) == len(expected_result)

    # check all the items in the result
    for word in expected_result:
        assert word in result


def test_find_tech_terms_pool_threads():
    """test find_tech_terms_pool_threads: handle multiple jobs listings at once with threads pool"""
    start_time = time.time()
    tech_set = get_tech_set()
    result = find_tech_terms_pool_threads(sample_data_developer_job_listings, tech_set)
    end_time = time.time()
    total_time = end_time - start_time

    # check all the jobs finished in less than the desired time
    assert total_time <= max_time_for_handling_multiple_listings_in_seconds
    # check all the jobs finished
    assert len(result) == len(sample_data_developer_job_listings)


if __name__ == '__main__':
    pytest.main()
