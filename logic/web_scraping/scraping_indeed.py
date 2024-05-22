"""This is a module to handle web scraping from indeed.com"""
import time
from models.Job_listing_site import JobListingSite
from chrome_driver_config import initialize_headless_chrome_driver
from selenium import webdriver  # Importing webdriver from Selenium library for web automation
# from selenium.webdriver.common.by import By  # Importing By class for locating elements
from selenium.webdriver.support.ui import WebDriverWait  # Importing WebDriverWait for waiting for elements
from selenium.webdriver.support import \
    expected_conditions as EC  # Importing expected_conditions for defining expected conditions


def extract_full_job_description(site: JobListingSite):
    """a function that extract a job description from a site"""
    # Initialize the chrome driver service
    start_time = time.time()
    webdriver_service, chrome_options = initialize_headless_chrome_driver()
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    # open the job URL
    driver.get(site.url)
    try:
        job_description_div = (WebDriverWait(driver, 10).
                               until(EC.presence_of_element_located((site.full_description_element_type,
                                                                     site.full_description_element_identifier))))

        # # find the job description element
        job_description_text: str = job_description_div.text.strip()
        print(job_description_text)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function  executed in {execution_time:.2f} seconds")
        return

    finally:
        driver.quit()


def contains(a: str, b: str):
    print(a.__contains__(b))


def main():
    pass


if __name__ == "__main__":
    main()
