"""This is a module to handle web scraping from indeed.com"""
import time

from selenium.common import TimeoutException
from chrome_driver_config import initialize_headless_chrome_driver
from selenium import webdriver  # Importing webdriver from Selenium library for web automation
from selenium.webdriver.common.by import By  # Importing By class for locating elements
from selenium.webdriver.chrome.service import Service  # Importing Service class for configuring Chrome driver service
from selenium.webdriver.chrome.options import Options  # Importing Options class for configuring Chrome browser options
from selenium.webdriver.support.ui import WebDriverWait  # Importing WebDriverWait for waiting for elements
from selenium.webdriver.support import \
    expected_conditions as EC  # Importing expected_conditions for defining expected conditions
from bs4 import BeautifulSoup  # Importing BeautifulSoup for parsing HTML content
import concurrent.futures  # Importing concurrent.futures for concurrent execution
from decorators.messure_function_time_dec import measure_function_time
import requests


def extract_full_job_description(job_url: str, element_identifier: str, byType: str):
    """a function that extract a job description from a site"""
    # Initialize the chrome driver service
    start_time = time.time()
    webdriver_service, chrome_options = initialize_headless_chrome_driver()
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    # open the job URL
    driver.get(job_url)
    # job_description_css_selector_id = "jobDescriptionText"
    job_description_css_selector_id = "JobDetails_jobDetailsContainer__y9P3L"
    try:
        job_description_div = (WebDriverWait(driver, 10).
                               until(EC.presence_of_element_located((byType,element_identifier))))
        # # find the job description element
        job_description_text: str = job_description_div.text.strip()
        print(job_description_text)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function  executed in {execution_time:.2f} seconds")
        return


    finally:
        driver.quit()


def main():
    indeed_job_url = 'https://il.indeed.com/jobs?q=backend+developer&l=&from=searchOnHP&vjk=c4417f57a461ea85'
    indeed_element_name = 'jobDescriptionText'
    indeed_element_type = By.ID
    glassdoor_job_url = 'https://www.glassdoor.com/Job/israel-backend-developer-jobs-SRCH_IL.0,6_IN119_KO7,24.htm'
    glassdoor_element_name = 'JobDetails_jobDetailsContainer__y9P3L'
    glassdoor_element_type = By.CLASS_NAME
    extract_full_job_description(indeed_job_url, indeed_element_name, indeed_element_type)
    extract_full_job_description(glassdoor_job_url, glassdoor_element_name, glassdoor_element_type)


if __name__ == "__main__":
    main()
