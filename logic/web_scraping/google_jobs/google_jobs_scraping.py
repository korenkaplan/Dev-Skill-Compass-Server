""" this module is dedicated to script job listings from google jobs"""
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from logic.web_scraping.DTOS.google_jobs_configuration_dto import GoogleJobsConfigDto


def countdown(n):
    for i in range(n, 0, -1):
        print(f"\r{i}", end="", flush=True)
        time.sleep(1)
    print("\r0", flush=True)  # Ensure the last number is also printed on the same line


def click_button(xpath, driver, timeout=1.0) -> (bool, str):
    try:
        # Wait for the button to be present in the DOM
        button = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

        # Once present, wait for it to be clickable
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        # Click the button
        button.click()
        return True, ''
    except TimeoutException:
        error = "click_button() -> Timed out waiting for button to be present or clickable"
        return False, error
    except NoSuchElementException:
        error = "click_button() -> Button not found"
        return False, error
    except ElementClickInterceptedException:
        error = "click_button() -> Button click intercepted"
        return False, error


def get_full_description(xpath, _driver) -> (bool, str):
    try:
        # Wait for the element to be present in the DOM
        element = WebDriverWait(_driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        error = "get_full_description() -> Timed out waiting for element to be present"
        return False, error
    try:
        # Once present, wait for it to be visible
        WebDriverWait(_driver, 10).until(EC.visibility_of(element))
    except TimeoutException:
        error = "get_full_description() -> Timed out waiting for element to be visible"
        return False, error

    try:
        # Retrieve and return the text of the element
        description = element.text
        if description:
            return True, description
        else:
            error = "get_full_description() -> Element is present but contains no text."
            return False, error
    except Exception as e:
        error = f"get_full_description() -> An error occurred: {e}"
        return False, error


def write_text_to_file(filepath: str, mode: str, text: str, seperator_sign='=', seperator_length=300, encoding='utf-8',
                       add_time_stamp=True) -> bool:
    try:
        seperator = seperator_length * seperator_sign
        with open(filepath, mode, encoding=encoding) as file:
            if add_time_stamp:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                file.write(f"({timestamp}) -> {text}\n")
            else:
                file.write(f"{text} \n")
            if seperator:
                file.write(seperator + '\n')
        return True
    except Exception as e:
        print("An error occurred: ", e)
        return False


def setup_chrome_driver(params=None, set_auto_params=True, activate=False, url='', headless=True) -> WebDriver:
    if params is None and set_auto_params is True:
        params = {
            "latitude": 32.109333,
            "longitude": 34.855499,
            "accuracy": 100
        }

    if headless:
        chrome_options = Options()
        chrome_headless_arguments = ('--headless', '--no-sandbox', '--disable-dev-shm-usage',
                                     "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        for option in chrome_headless_arguments:
            chrome_options.add_argument(option)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    else:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
    if activate:
        if len(url) > 0:
            driver.get(url)
        else:
            print('Could not activate driver url is necessary')

    if activate is False and len(url) > 0:
        print('Could not activate driver: activate is set to False')

    return driver


def build_google_jobs_url(search_value: str, googleJobsTimePeriod: GoogleJobsTimePeriod, replace_with_char='+') -> str:
    snake_case_search_value = search_value.replace(' ', replace_with_char)
    time_period = googleJobsTimePeriod.value
    url = f"""https://www.google.com/search?q={snake_case_search_value}
    +jobs+israel&ibp=htl;jobs&hl=en&gl=us#fpstate=tldetail&=&=&htivrt=jobs&htichips=
    date_posted:{time_period}&htischips=date_posted;{time_period}"""

    return url


def setup_web_driver_wait(driver: WebDriver, timeout=10) -> WebDriverWait[WebDriver | WebElement]:
    return WebDriverWait(driver, timeout)


# region Sub scroll_and_click_and_visited_pipeline
def scroll_element_to_view(element: WebElement, driver: WebDriver) -> bool:
    try:
        # Scroll to view
        driver.execute_script("arguments[0].scrollIntoView();", element)
        return True

    except StaleElementReferenceException:
        return False


def is_listing_visited(url: str, visited_urls: set[str]):
    if url in visited_urls:
        return True
    else:
        visited_urls.add(url)
        return False


def scroll_and_click_and_visited_pipeline(driver: WebDriver, job_listing_element: WebElement, visited_urls: set[str],
                                          log_file_path: str) -> int:
    try:
        # scroll to view the element
        is_scrolled = scroll_element_to_view(job_listing_element, driver)

        if is_scrolled is False:
            write_text_to_file(log_file_path, 'a',
                               'StaleElementReferenceException: Element no longer'
                               ' exists in the dom problem fetching list to soon error')
            return 0

        # click the element for the full description to appear and change the url
        job_listing_element.click()

        # get the url from driver and check if it has been visited
        url = driver.current_url
        is_visited = is_listing_visited(url, visited_urls)

        if is_visited:
            write_text_to_file(log_file_path, 'a',
                               f"Scraping has Repeated this url: {url}")
            return 1

        return 2

    except Exception as e:
        # Handle any other exceptions that may occur
        write_text_to_file(log_file_path, 'a',
                           f"scroll_and_click_and_visited_pipeline() - > An error occurred: {str(e)}")
        return 0


# endregion

# region get initial job listings li elements
def get_job_listings_li_elements_list(wait: WebDriverWait, log_file_path: str) -> list[WebElement]:
    try:
        job_listings = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li")))
        return job_listings if job_listings is not None else []
    except TimeoutException:
        write_text_to_file(log_file_path, 'a', "Job listings did not appear within the timeout period.")
        return []


# endregion

# region get description and show more button
def get_description(driver: WebDriver, expand_job_description_button_xpath: str, expandable_job_description_xpath: str,
                    not_expanded_job_description_xpath: str, click_button_timeout: float, log_file_path: str):
    try:
        is_clicked, result_message_click_button = click_button(expand_job_description_button_xpath, driver,
                                                               timeout=click_button_timeout)
        if is_clicked:
            is_successful, description = get_full_description(expandable_job_description_xpath, driver)
        else:
            is_successful, description = get_full_description(not_expanded_job_description_xpath, driver)

        if is_successful is False:
            write_text_to_file(log_file_path, 'a', description)

        return is_successful, description

    except NoSuchElementException:
        write_text_to_file(log_file_path, 'a',
                           'NoSuchElementException: did not find button or description check logs')
        return False, "Failed"


# endregion


def get_job_listings(driver: WebDriver, wait: WebDriverWait, expand_job_description_button_xpath: str,
                     expandable_job_description_xpath: str, log_file_path: str,
                     not_expanded_job_description_xpath: str, click_button_timeout=1.0,
                     ) -> list[str]:
    # get the initial job_listings visible on page load
    job_listings = get_job_listings_li_elements_list(wait, log_file_path)
    if len(job_listings) == 0:
        driver.quit()
        return []

    # if successful init variables
    (skip_amount, previous_size, inserted_descriptions,
     job_listings_result_list, urls_attempted_set) = 0, -1, 0, [], set()

    while job_listings:
        # If the previous size is the same as the current size, there are no more job listings to load
        if previous_size == len(job_listings):
            break
        # update the size after the check
        previous_size = len(job_listings)

        # Iterate through each job listing, skipping the previously clicked ones
        for i in range(skip_amount, len(job_listings)):

            result: int = scroll_and_click_and_visited_pipeline(driver, job_listings[i], urls_attempted_set,
                                                                log_file_path)
            if result == 0:
                driver.quit()
                return []
            elif result == 1:
                continue

            is_successful, description = get_description(driver, expand_job_description_button_xpath,
                                                         expandable_job_description_xpath,
                                                         not_expanded_job_description_xpath,
                                                         click_button_timeout,
                                                         log_file_path)

            if is_successful:
                job_listings_result_list.append(description)
                inserted_descriptions += 1

            # Update the skip amount for the next iteration
            skip_amount = len(job_listings)

        # Refind the job listings to avoid StaleElementReferenceException
        job_listings = driver.find_elements(By.CSS_SELECTOR, "li")

    # log the final result of the function how many listings were collected
    text = f"Inserted descriptions: {inserted_descriptions}, job_listings:{len(job_listings)}"
    write_text_to_file(log_file_path, 'a', text)

    return job_listings_result_list


def get_job_listings_google_jobs_pipeline(config_object: GoogleJobsConfigDto) -> list[str]:
    # region params
    listings_list = []
    interval_attempts = 0
    is_success = False
    click_button_timeout = 1
    url = build_google_jobs_url(config_object.search_value, config_object.time_period)
    driver = setup_chrome_driver(url=url, activate=True)
    wait = setup_web_driver_wait(driver, 3)
    # endregion

    # create intervals
    while is_success is False and interval_attempts < config_object.max_interval_attempts:
        if interval_attempts > 0:
            print("Interval attempt failed retry in: ")
            countdown(config_object.sleep_time_between_attempt_in_seconds)
            driver = setup_chrome_driver(url=url, activate=True)
            wait = setup_web_driver_wait(driver, 10)

        interval_attempts += 1
        text = 'Attempt number: %d' % interval_attempts
        write_text_to_file(config_object.log_file_path, 'a', text)
        listings_list = get_job_listings(driver, wait, config_object.show_full_description_button_xpath,
                                         config_object.expandable_job_description_text_xpath,
                                         config_object.log_file_path,
                                         config_object.not_expandable_job_description_text_xpath, click_button_timeout)

        if len(listings_list) > 0:
            is_success = True

    # check the results after the while loop
    if is_success is False:
        text = 'Failed to scrape job listings after maximum attempts(%d)' % config_object.max_interval_attempts
        write_text_to_file(config_object.log_file_path, 'a', text)

    return listings_list
