""" this module is dedicated to script job listings from google jobs"""
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager

from decorators.decorator_measure_function_time import measure_function_time
import os
from dotenv import load_dotenv

load_dotenv()


class GoogleJobsTimePeriod(Enum):
    TODAY = 'today'
    THREE_DAYS = '3days'
    WEEK = 'week'
    MONTH = 'month'


def click_button(xpath, _driver, timeout=1.0) -> bool:
    try:
        # Wait for the button to be present in the DOM
        button = WebDriverWait(_driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

        # Once present, wait for it to be clickable
        WebDriverWait(_driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        # Click the button
        button.click()
        return True
    except TimeoutException as e:
        error = f"Timed out waiting for button to be present or clickable: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error)
        return False
    except NoSuchElementException as e:
        error = f"Button not found: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error)
        return False
    except ElementClickInterceptedException as e:
        error = f"Button click intercepted: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error)
        return False
    except Exception as e:
        error = f"An error occurred: {e}"
        write_text_to_file('click_button_logs.txt', 'a', error)
        return False


def get_full_description(xpath, _driver):
    try:
        # Wait for the element to be present in the DOM
        element = WebDriverWait(_driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException as e:
        error = f"Timed out waiting for element to be present: {e}"
        write_text_to_file('get_full_description_logs.txt', 'a', error)
    try:
        # Once present, wait for it to be visible
        WebDriverWait(_driver, 10).until(EC.visibility_of(element))
    except TimeoutException as e:
        error = f"Timed out waiting for element to be visible: {e}"
        write_text_to_file('get_full_description_logs.txt', 'a', error)

    try:
        # Retrieve and return the text of the element
        description = element.text
        if description:
            return description
        else:
            error = "Element is present but contains no text."
            write_text_to_file('get_full_description_logs.txt', 'a', error)
    except Exception as e:
        error = f"An error occurred: {e}"
        write_text_to_file('get_full_description_logs.txt', 'a', error)


def write_text_to_file(filepath: str, mode: str, text: str, seperator_sign='=', seperator_length=300, encoding='utf-8') -> bool:
    try:
        seperator = seperator_length * seperator_sign
        with open(filepath, mode, encoding=encoding) as file:
            file.write(text + '\n')
            if seperator:
                file.write(seperator + '\n')
        return True
    except Exception as e:
        print("An error occurred: ", e)
        return False


def setup_chrome_driver(params: dict) -> WebDriver:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
    return driver


def setup_and_activate_chrome_driver(url: str, params=None, set_auto_params=True) -> WebDriver:
    if params is None and set_auto_params is True:
        params = {
            "latitude": 32.109333,
            "longitude": 34.855499,
            "accuracy": 100
        }

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
    driver.get(url)
    return driver


def build_google_jobs_url(search_value: str, googleJobsTimePeriod: GoogleJobsTimePeriod, replace_with_char='+') -> str:
    snake_case_search_value = search_value.replace(' ', replace_with_char)
    time_period = googleJobsTimePeriod.value
    url = (f"""
    https://www.google.com/search?q={snake_case_search_value}+jobs+israel&ibp=htl;jobs&hl=en&gl=us#fpstate=tldetail&=&=&htivrt=jobs&htichips=date_posted:{time_period}&htischips=date_posted;{time_period}&htidocid=nPmFkUrgbES8cLN1AAAAAA%3D%3D
    """)
    return url


def setup_web_driver_wait(driver: WebDriver, timeout=10) -> WebDriverWait[WebDriver | WebElement]:
    return WebDriverWait(driver, timeout)


def get_job_listings(driver: WebDriver, wait: WebDriverWait, expand_job_description_button_xpath: str,
                     expandable_job_description_xpath: str,
                     not_expanded_job_description_xpath: str, click_button_timeout=1.0) -> list[str]:
    try:
        job_listings = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li")))
    except TimeoutException:
        print("Job listings did not appear within the timeout period.")
        driver.quit()
        exit()

    skip_amount = 0
    previous_size = -1
    inserted_descriptions = 0
    job_listings_result_list = []
    while job_listings:
        # If the previous size is the same as the current size, there are no more job listings to load
        if previous_size == len(job_listings):
            break

        previous_size = len(job_listings)
        # Iterate through each job listing, skipping the previously clicked ones
        for i in range(skip_amount, len(job_listings)):
            # Scroll to view
            driver.execute_script("arguments[0].scrollIntoView();", job_listings[i])
            # Click on the listing
            job_listings[i].click()

            try:
                is_clicked = click_button(expand_job_description_button_xpath, driver, timeout=click_button_timeout)
                if is_clicked:
                    description = get_full_description(expandable_job_description_xpath, driver)
                else:
                    description = get_full_description(not_expanded_job_description_xpath, driver)

                if description:
                    inserted_descriptions += 1
                    job_listings_result_list.append(description)

            except NoSuchElementException:
                print("Target element not found!")

            # Update the skip amount for the next iteration
            skip_amount = len(job_listings)

        # Refind the job listings to avoid StaleElementReferenceException
        job_listings = driver.find_elements(By.CSS_SELECTOR, "li")

    print(
        f"Inserted descriptions: {inserted_descriptions}, job_listings:{len(job_listings)}")
    return job_listings_result_list


@measure_function_time
def main():
    # region params
    # Define the search key and time period
    search_value = 'backend developer'
    time_period = GoogleJobsTimePeriod.MONTH
    button_full_xpath = os.environ.get('SHOME_FULL_DESCRIPTION_BUTTON_XPATH_GOOGLE_JOBS')
    expandable_text_full_xpath = os.environ.get('EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS')
    not_expandable_text_full_xpath = os.environ.get('NOT_EXPANDABLE_JOB_DESCRIPTION_TEXT_XPATH_GOOGLE_JOBS')
    # endregion

    url = build_google_jobs_url(search_value, time_period)
    driver = setup_and_activate_chrome_driver(url)
    wait = setup_web_driver_wait(driver, 10)
    listings_list = get_job_listings(driver, wait, button_full_xpath,
                                     expandable_text_full_xpath,
                                     not_expandable_text_full_xpath, 1)

    for job in listings_list:
        write_text_to_file('descriptions.txt', 'a', job)



if __name__ == '__main__':
    main()

"""
Add retry if loading at first not working
check if a job listing is repeated with set of urls
"""
