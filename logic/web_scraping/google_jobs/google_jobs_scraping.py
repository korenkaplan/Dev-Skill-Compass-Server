""" this module is dedicated to script job listings from Google jobs"""

import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from init_db.data.data import get_words_to_remove_from_title
from logic.web_scraping.DTOS.enums import GoogleJobsTimePeriod
from logic.web_scraping.google_jobs.DTO.google_jobs_configuration_dto import (
    GoogleJobsConfigDto,
)
from logic.web_scraping.google_jobs.DTO.google_jobs_get_full_description_dto import (
    GoogleJobsGetFullDescriptionDto,
)
from logic.web_scraping.google_jobs.DTO.google_jobs_get_job_listings_dto import (
    GoogleJobsGetJobListingsDto,
)
from logic.web_scraping.google_jobs.DTO.google_jobs_title_element_xpath_dto import (
    GoogleJobsTitleElementXpathDto,
)
from utils.functions import write_text_to_file, countdown

# region Elements interaction functions
def click_button(xpath, driver, timeout=1.0) -> (bool, str):
    """
    Attempts to click a button located by its XPath within a given timeout.

    Args:
        xpath (str): The XPath of the button to click.
        driver (WebDriver): The Selenium WebDriver instance.
        timeout (float): Maximum time to wait for the button to be clickable.

    Returns:
        tuple: A tuple containing a boolean indicating success or failure, and an error message if applicable.
    """
    try:
        # Wait for the button to be present in the DOM
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # Once present, wait for it to be clickable
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        # Click the button
        button.click()
        return True, ""
    except TimeoutException:
        error = (
            "click_button() -> Timed out waiting for button to be present or clickable"
        )
        return False, error
    except NoSuchElementException:
        error = "click_button() -> Button not found"
        return False, error
    except ElementClickInterceptedException:
        error = "click_button() -> Button click intercepted"
        return False, error


def get_full_description(xpath, _driver) -> (bool, str):
    """
    Retrieves the full text description of an element located by its XPath.

    Args:
        xpath (str): The XPath of the element to retrieve text from.
        _driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        tuple: A tuple containing a boolean indicating success or failure,
         and the text or an error message if applicable.
    """
    try:
        # Wait for the element to be present in the DOM
        element = WebDriverWait(_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
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


# endregion


# region Setup and Initialization functions
def setup_chrome_driver(
    params=None, set_auto_params=True, activate=False, url="", headless=False
) -> WebDriver:
    """
    Sets up a Chrome WebDriver with optional geolocation parameters and headless mode.

    Args:
        params (dict): Geolocation parameters with keys 'latitude', 'longitude', and 'accuracy'.
        set_auto_params (bool): Whether to automatically set default geolocation parameters.
        activate (bool): Whether to open the browser and navigate to the specified URL.
        url (str): The URL to navigate to if activate is True.
        headless (bool): Whether to run the browser in headless mode.

    Returns:
        WebDriver: The configured Selenium WebDriver instance.
    """
    if params is None and set_auto_params is True:
        params = {"latitude": 32.109333, "longitude": 34.855499, "accuracy": 100}

    if headless:
        chrome_options = Options()
        chrome_headless_arguments = (
            "--headless",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )
        for option in chrome_headless_arguments:
            chrome_options.add_argument(option)
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )
    else:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
        driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
    if activate:
        if len(url) > 0:
            driver.get(url)
        else:
            print("Could not activate driver url is necessary")

    if activate is False and len(url) > 0:
        print("Could not activate driver: activate is set to False")

    return driver


def build_google_jobs_url(
    search_value: str, googleJobsTimePeriod: GoogleJobsTimePeriod, replace_with_char="+"
) -> str:
    """
    Builds a Google Jobs URL based on the search value and time period.

    Args:
        search_value (str): The job search query.
        googleJobsTimePeriod (enum): The time period filter for the job search.
        replace_with_char (str): Character to replace spaces in the search query.

    Returns:
        str: The constructed Google Jobs URL.
    """
    snake_case_search_value = search_value.replace(" ", replace_with_char)
    time_period = googleJobsTimePeriod.value
    url = (f"https://www.google.com/search?q={snake_case_search_value}+jobs+israel&ibp=htl;"
           f"jobs&hl=en&gl=us#fpstate=tldetail&=&=&htivrt=jobs&htichips=date_posted:{time_period}&"
           f"htischips=date_posted;{time_period}")
    return url


def setup_web_driver_wait(
    driver: WebDriver, timeout=10
) -> WebDriverWait[WebDriver | WebElement]:
    """
    Sets up a WebDriverWait instance for the given WebDriver.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        timeout (int): The maximum wait time in seconds.

    Returns:
        WebDriverWait: The WebDriverWait instance configured with the timeout.
    """
    return WebDriverWait(driver, timeout)


# endregion


# region Sub scroll_and_click_and_visited_pipeline
def scroll_element_to_view(element: WebElement, driver: WebDriver) -> bool:
    """
    Scrolls a web element into view.

    Args:
        element (WebElement): The web element to scroll into view.
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        bool: True if the element was scrolled into view successfully, False otherwise.
    """
    try:
        # Scroll to view
        driver.execute_script("arguments[0].scrollIntoView();", element)
        return True

    except StaleElementReferenceException:
        return False


def is_listing_visited(url: str, visited_urls: set[str]):
    """
    Checks if a URL has been visited and updates the visited URLs set.

    Args:
        url (str): The URL to check.
        visited_urls (set[str]): The set of visited URLs.

    Returns:
        bool: True if the URL has been visited, False otherwise.
    """
    if url in visited_urls:
        return True
    else:
        visited_urls.add(url)
        return False


def scroll_and_click_and_visited_pipeline(
    driver: WebDriver,
    job_listing_element: WebElement,
    visited_urls: set[str],
    log_file_path: str,
) -> int:
    """
    Scrolls a job listing element into view, clicks it, and checks if the URL has been visited.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        job_listing_element (WebElement): The job listing element to interact with.
        visited_urls (set[str]): The set of visited URLs.
        log_file_path (str): The path to the log file.

    Returns:
        int: A status code indicating the result (0: error, 1: URL already visited, 2: success).
    """
    try:
        # scroll to view the element
        is_scrolled = scroll_element_to_view(job_listing_element, driver)

        if is_scrolled is False:
            write_text_to_file(
                log_file_path,
                "a",
                "StaleElementReferenceException: Element no longer"
                " exists in the dom problem fetching list to soon error",
            )
            return 0

        # click the element for the full description to appear and change the url
        job_listing_element.click()

        # get the url from driver and check if it has been visited
        url = driver.current_url
        is_visited = is_listing_visited(url, visited_urls)

        return 1 if is_visited else 2

    except Exception as e:
        # Handle any other exceptions that may occur
        write_text_to_file(
            log_file_path,
            "a",
            f"scroll_and_click_and_visited_pipeline() - > An error occurred: {str(e)}",
        )
        return 0


# endregion


# region get initial job listings li elements
def get_job_listings_li_elements_list(
    wait: WebDriverWait, log_file_path: str
) -> list[WebElement]:
    """
    Retrieves a list of job listing <li> elements.

    Args:
        wait (WebDriverWait): The WebDriverWait instance to use for waiting.
        log_file_path (str): The path to the log file.

    Returns:
        list[WebElement]: A list of job listing elements, or an empty list if none were found.
    """
    try:
        job_listings = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "li"))
        )
        return job_listings if job_listings is not None else []
    except TimeoutException:
        write_text_to_file(
            log_file_path, "a", "Job listings did not appear within the timeout period."
        )
        return []


# endregion


# region get description and show more button
def get_description(dto: GoogleJobsGetFullDescriptionDto):
    """
    Retrieves the job description by first attempting to expand it if possible.

    Args:
        dto: GoogleJobsGetFullDescriptionDto object

    Returns:
        tuple: A tuple containing a boolean indicating success or failure, and the job description or an error message.

    """
    try:
        is_clicked, result_message_click_button = click_button(
            dto.expand_job_description_button_xpath,
            dto.driver,
            timeout=dto.click_button_timeout,
        )
        if is_clicked:
            is_successful, description = get_full_description(
                dto.expandable_job_description_xpath, dto.driver
            )
        else:
            is_successful, description = get_full_description(
                dto.not_expanded_job_description_xpath, dto.driver
            )

        if is_successful is False:
            write_text_to_file(dto.log_file_path, "a", description)

        return is_successful, description

    except NoSuchElementException:
        write_text_to_file(
            dto.log_file_path,
            "a",
            "NoSuchElementException: did not find button or description check logs",
        )
        return False, "Failed"


# endregion

# region title fetching


# build the xpath to the title div
def build_listing_title_xpath_arguments(
    i: int, increase_every_ten: int
) -> (int, str, int, bool, int):
    only_first_is_one_else_2 = 1 if i == 0 else 2
    # extra_div = '/div' if increase_every_ten > 5 else ''
    extra_div = ""
    one_to_ten = i % 10 + 1
    increase_every_ten += 1 if i % 10 == 0 else 0
    is_wait = one_to_ten == 1

    return only_first_is_one_else_2, extra_div, one_to_ten, is_wait, increase_every_ten


# search the title with the web driver
def find_title(find_title_dto: GoogleJobsTitleElementXpathDto) -> str:
    xpath = (
        f'//*[@id="VoQFxe"]/div[{find_title_dto.increase_every_ten}]/div/ul/li[{find_title_dto.one_to_ten}]'
        f"/div/div[{find_title_dto.only_first_is_one_else_2}]/div[2]/div/div/div{find_title_dto.extra_div}[2]/div[2]"
    )

    retries = 3  # Number of retries for handling StaleElementReferenceException
    for _ in range(retries):
        if find_title_dto.is_wait:
            time.sleep(2)
        try:
            title = find_title_dto.listing_li_element.find_element(
                By.XPATH, xpath
            ).get_attribute("innerText")
            return title
        except StaleElementReferenceException:
            print("StaleElementReferenceException caught. Retrying...")
        except TimeoutException:
            print("TimeoutException caught. Retrying...")
        except NoSuchElementException:
            print("NoSuchElementException caught. Retrying...")


# Get the list of general words to remove by role
def get_list_value_by_key(
    role: str, roles_words_dict: dict[str: list[str]]
) -> list[str]:
    if role in roles_words_dict:
        return roles_words_dict[role]

    else:
        print(f"{role} key is not found in the dictionary returned empty list")
        return []


# Remove the general words
def remove_words(text: str, words: list) -> str:
    # remove all the common words
    for word in words:
        text = text.replace(word, "").strip()
        text = text.replace(" ", "")

    return text


# clean the text to letters only
def remove_non_letters_characters(text: str) -> str:
    # remove everything beside letters
    only_letters_regex_pattern = r"[^a-zA-Z]"
    result = re.sub(only_letters_regex_pattern, "", text)
    return result


def is_title_match_role(role: str, title: str, log_file_path: str, false_title_counter: int) -> (bool, int):
    # Get the words to remove from the title by role
    words_to_remove = get_words_to_remove_from_title(role)

    # Remove the words from the title
    cleaned_title = remove_words(title.lower(), words_to_remove)
    cleaned_role = remove_words(role.lower(), words_to_remove)

    # Clean the non alphabet letters
    cleaned_role = remove_non_letters_characters(cleaned_role)
    cleaned_title = remove_non_letters_characters(cleaned_title)

    # Check if the cleaned role is in the cleaned title
    res = cleaned_role in cleaned_title

    # log if not matched
    if res is False:
        log_text = (
            f"""False match: {cleaned_title}({title} <-> {cleaned_role}({role})"""
        )
        write_text_to_file(log_file_path, "a", log_text)
        false_title_counter += 1

    return res, false_title_counter


def find_and_match_title(
    role: str,
    i: int,
    increase_every_ten: int,
    listing_li_element: WebElement,
    wait: WebDriverWait,
    log_file_path: str,
    false_title_counter: int
) -> (bool, int):
    # Define the result variables
    is_title_exist = False
    is_match = False

    # build the xpath to the element
    only_first_is_one_else_2, extra_div, one_to_ten, is_wait, increase_every_ten = (
        build_listing_title_xpath_arguments(i, increase_every_ten)
    )
    # Create the dto object
    dto: GoogleJobsTitleElementXpathDto = GoogleJobsTitleElementXpathDto(
        wait=wait,
        listing_li_element=listing_li_element,
        increase_every_ten=increase_every_ten,
        one_to_ten=one_to_ten,
        only_first_is_one_else_2=only_first_is_one_else_2,
        extra_div=extra_div,
        is_wait=is_wait,
    )
    # try to get the title from the element
    title = find_title(dto)

    if title:
        is_match = is_title_match_role(role, title, log_file_path, false_title_counter)
        is_title_exist = True

    if not is_title_exist:
        print("Could not find title element")

    return is_match, increase_every_ten, false_title_counter


# endregion


def get_job_listings(dto: GoogleJobsGetJobListingsDto) -> list[str]:
    """
    Retrieves job listings and their descriptions from a webpage.

    Args:
         dto: GoogleJobsGetJobList dto object
    Returns:
        list[str]: A list of job descriptions retrieved from the job listings.

    """

    # get the initial job_listings visible on page load
    job_listings = get_job_listings_li_elements_list(dto.wait, dto.log_file_path)
    if len(job_listings) == 0:
        dto.driver.quit()
        return []
    # if successful init variables
    skip_amount = 0
    previous_size = -1
    inserted_descriptions = 0
    job_listings_result_list = []
    urls_attempted_set = set()
    false_title_counter = 0
    increase_every_ten = 0
    repeated_urls_counter = 0

    while job_listings:
        # If the previous size is the same as the current size, there are no more job listings to load
        if previous_size == len(job_listings):
            break
        # update the size after the check
        previous_size = len(job_listings)
        print(f"Total listings collected {dto.role}: {inserted_descriptions}")
        # Iterate through each job listing, skipping the previously clicked ones
        for i in range(skip_amount, len(job_listings)):
            # Start the process bys scrolling to view and clicking the listing
            result: int = scroll_and_click_and_visited_pipeline(
                dto.driver, job_listings[i], urls_attempted_set, dto.log_file_path
            )

            if result == 0:
                dto.driver.quit()
                return []

            elif result == 1:
                repeated_urls_counter += 1
                continue

            # find and match the title to the role
            is_title_match, increase_every_ten, false_title_counter = find_and_match_title(
                dto.role,
                i,
                increase_every_ten,
                job_listings[i],
                dto.wait,
                dto.log_file_path,
                false_title_counter
            )

            if is_title_match is False:
                continue

            get_full_description_dto: GoogleJobsGetFullDescriptionDto = (
                GoogleJobsGetFullDescriptionDto(
                    driver=dto.driver,
                    expand_job_description_button_xpath=dto.expand_job_description_button_xpath,
                    expandable_job_description_xpath=dto.expandable_job_description_xpath,
                    not_expanded_job_description_xpath=dto.not_expanded_job_description_xpath,
                    click_button_timeout=dto.click_button_timeout,
                    log_file_path=dto.log_file_path,
                )
            )
            # extrac the job description
            is_successful, description = get_description(get_full_description_dto)

            if is_successful:
                job_listings_result_list.append(description)
                inserted_descriptions += 1

            # Update the skip amount for the next iteration
            skip_amount = len(job_listings)

        # Refind the job listings to avoid StaleElementReferenceException
        job_listings = dto.driver.find_elements(By.CSS_SELECTOR, "li")

    # log the final result of the function how many listings were collected
    text = f"""
    Inserted descriptions: {inserted_descriptions} 
    Error titles counter: {false_title_counter} 
    Repeated URLS: {repeated_urls_counter}
    Problematic URLS: 1
    --------------------------------------
    Total Job Listings: {len(job_listings)}
"""
    write_text_to_file(dto.log_file_path, "a", text)

    return job_listings_result_list


def get_job_listings_google_jobs_pipeline(
    config_object: GoogleJobsConfigDto,
) -> list[str]:
    """
    Executes a pipeline to scrape job listings from Google Jobs based on the provided configuration.

    Args:
        config_object (GoogleJobsConfigDto): Configuration object containing search parameters and settings.

    Returns:
        list[str]: A list of job descriptions retrieved from Google Jobs.
    """
    # region params
    listings_list = []
    interval_attempts = 0
    is_success = False
    url = build_google_jobs_url(config_object.role, config_object.time_period)
    driver = setup_chrome_driver(url=url, activate=True)
    wait = setup_web_driver_wait(driver, 3)
    # endregion

    # create intervals
    while (
        is_success is False and interval_attempts < config_object.max_interval_attempts
    ):
        if interval_attempts > 0:
            print("Interval attempt failed retry in: ")
            countdown(config_object.sleep_time_between_attempt_in_seconds)
            driver = setup_chrome_driver(url=url, activate=True)
            wait = setup_web_driver_wait(driver, 10)

        interval_attempts += 1
        text = "Attempt number: %d" % interval_attempts
        write_text_to_file(config_object.log_file_path, "a", text)
        dto: GoogleJobsGetJobListingsDto = GoogleJobsGetJobListingsDto(
            role=config_object.role,
            driver=driver,
            wait=wait,
            expand_job_description_button_xpath=config_object.show_full_description_button_xpath,
            expandable_job_description_xpath=config_object.expandable_job_description_text_xpath,
            log_file_path=config_object.log_file_path,
            not_expanded_job_description_xpath=config_object.not_expandable_job_description_text_xpath,
            click_button_timeout=1.0,
        )
        listings_list = get_job_listings(dto)

        if len(listings_list) > 0:
            is_success = True

    # check the results after the while loop
    if is_success is False:
        text = (
            "Failed to scrape job listings after maximum attempts(%d)"
            % config_object.max_interval_attempts
        )
        write_text_to_file(config_object.log_file_path, "a", text)

    return listings_list
