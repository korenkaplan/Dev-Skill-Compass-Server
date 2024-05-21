"""This is a module to handle web scraping from indeed.com"""
import time
from models.Job_listing_site import JobListingSite
from selenium.common import TimeoutException, NoSuchElementException
from chrome_driver_config import initialize_headless_chrome_driver
from selenium import webdriver  # Importing webdriver from Selenium library for web automation
from selenium.webdriver.common.by import By  # Importing By class for locating elements
from selenium.webdriver.chrome.service import Service  # Importing Service class for configuring Chrome driver service
from selenium.webdriver.chrome.options import Options  # Importing Options class for configuring Chrome browser options
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
                               until(EC.presence_of_element_located((site.full_description_element_type, site.full_description_element_identifier))))
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
    indeed = JobListingSite('indeed', 'https://il.indeed.com/jobs?q=backend+developer&l=&from=searchOnHP&vjk=c4417f57a461ea85', 'jobDescriptionText',  By.ID)
    glassdoor = JobListingSite('glassdoor', 'https://www.glassdoor.com/Job/israel-backend-developer-jobs-SRCH_IL.0,6_IN119_KO7,24.htm', 'JobDetails_jobDetailsContainer__y9P3L', By.CLASS_NAME)
    google_for_jobs = JobListingSite('google_for_jobs', 'https://www.google.com/search?q=backend+developer+&ibp=htl;jobs&hl=en&gl=us#fpstate=tldetail&htivrt=jobs&htichips=date_posted:week&htischips=date_posted;week&htidocid=EXVQoJ1pR8ly3_foAAAAAA%3D%3D',

if __name__ == "__main__":
    main()
