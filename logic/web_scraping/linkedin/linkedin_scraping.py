# region WSGI
"""
WSGI config for django_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import re
import time

from django.core.wsgi import get_wsgi_application

from utils.functions import write_text_to_file

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_server.settings")

application = get_wsgi_application()
# endregion

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
from logic.web_scraping.linkedin.DTO.linkedin_get_job_listings_dto import LinkedinGetJobListingsDto
from utils.enums import LinkedinTimePeriod
from init_db.data.data import get_words_to_remove_from_title, get_synonyms_words_title
import requests
from bs4 import BeautifulSoup
from lxml import etree




# region Setup and Initialization functions
def build_url_linkedin(search_value: str, linkedin_time_period: LinkedinTimePeriod,
                       replace_space_with_char='%20') -> str:
    pass


def setup_chrome_driver(activate=False, url="", headless=False) -> WebDriver:
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
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    if activate:
        if len(url) > 0:
            driver.get(url)
        else:
            print("Could not activate driver url is necessary")

    if activate is False and len(url) > 0:
        print("Could not activate driver: activate is set to False")

    return driver


def setup_web_driver_wait(driver: WebDriver, timeout=3):
    return WebDriverWait(driver, timeout)


# endregion


def get_full_description(description_div_xpath: str, show_more_button_xpath: str, wait: WebDriverWait) -> (bool, str):
    # init the variables
    job_details_text = ""
    text_sections: list = []
    try:
        # find the description div and the show more button
        element = wait.until((EC.visibility_of_element_located((By.XPATH, description_div_xpath))))
        button = wait.until((EC.visibility_of_element_located((By.XPATH, show_more_button_xpath))))

        # click the show more button
        button.click()

        # find all the text elements inside the div
        text_sections.extend(element.find_elements(By.CSS_SELECTOR, "p"))
        text_sections.extend(element.find_elements(By.CSS_SELECTOR, "li"))

        # add the text of the elements to the result
        for p_tag in text_sections:
            job_details_text += f"{p_tag.text}"
        print(job_details_text)
        return True, job_details_text
    except Exception as e:
        print(f"Function: get_full_description -> error: {e}")
        return False, job_details_text



def get_job_listings_li_elements_list(result_list_xpath: str, wait: WebDriverWait) -> list[WebElement]:
    try:
        # find the list elements
        result_list: WebElement = wait.until((EC.visibility_of_element_located((By.XPATH, result_list_xpath))))

        # find all the li elements in the result list
        listing_li_elements: list[WebElement] = result_list.find_elements(By.CSS_SELECTOR, 'li')

        return listing_li_elements

    except Exception as e:
        print(f"Function: get_all_listings_list -> error: {e}")
        return []


def scroll_element_to_view(element: WebElement, driver: WebDriver) -> bool:
    try:
        # Scroll to view
        driver.execute_script("arguments[0].scrollIntoView();", element)
        return True

    except StaleElementReferenceException:
        return False


def is_listing_visited(url: str, visited_urls: set[str]) -> bool:
    if url in visited_urls:
        return True
    else:
        visited_urls.add(url)
        return False


def scroll_and_click_and_visited_pipeline(driver: WebDriver, job_listing_li_element: WebElement,
                                          visited_urls: set[str]) -> int:
    try:
        # scroll to view the element
        is_scrolled = scroll_element_to_view(job_listing_li_element, driver)

        if is_scrolled is False:
            print("Function: scroll_and_click_and_visited_pipeline error: is_scrolled is False")
            return 0

        # click the element for the full description to appear and change the url
        job_listing_li_element.click()

        # get the url from driver and check if it has been visited
        url = driver.current_url
        is_visited = is_listing_visited(url, visited_urls)

        # return the result
        return 1 if is_visited else 2

    except Exception as e:
        print(f"Function: scroll_and_click_and_visited_pipeline error: {e}")


def extract_title_from_li_element(listing_li_element: WebElement) -> str:
    try:
        span_element = listing_li_element.find_element(By.CSS_SELECTOR, 'span')
        if span_element:
            return span_element.text
        else:
            return ""
    except Exception as e:
        print(f"Function: extract_title_from_li_element error: {e}")


def format_role_title(title: str) -> str:
    # remove everything beside letters
    only_letters_regex_pattern = r"[^a-zA-Z]"
    result = re.sub(only_letters_regex_pattern, "", title)
    return result


def is_title_and_role_match(formatted_role: str, formatted_title: str) -> bool:
    pass


def remove_words(text: str, words: list) -> str:
    # remove all the common words
    for word in words:
        text = text.replace(word, "").strip()
        text = text.replace(" ", "")

    return text


def remove_non_letters_characters(text: str) -> str:
    # remove everything beside letters
    only_letters_regex_pattern = r"[^a-zA-Z]"
    result = re.sub(only_letters_regex_pattern, "", text)
    return result


def is_title_in_synonyms_words(role: str, clean_title: str) -> bool:
    # get the synonyms words for the role
    synonyms_words: list[str] = get_synonyms_words_title(role)

    # clean the words (remove spaces and to lower and signs)
    formatted_words: list[str] = [word.replace(" ", "").lower().strip() for word in synonyms_words]

    # compare each clean word against the cleaned title
    for word in formatted_words:
        if word in clean_title:
            return True
    # return false if not found
    return False


def is_title_match_role(role: str, title: str) -> bool:
    try:
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
        if res is False:
            res = is_title_in_synonyms_words(role, cleaned_title)

        if res is False:
            print(f"""False match: {cleaned_title}({title} <-> {cleaned_role}({role})""")

        return res
    except Exception as e:
        print(f"Function is_title_match_role error: {e}")
        return False


def find_and_match_title(role: str, i: int, listing_li_element: WebElement, wait: WebDriverWait) -> (bool, str):
    try:
        # Define the result variables
        is_title_exist = False
        is_match = False

        # extract the title string from the element
        title_from_li = extract_title_from_li_element(listing_li_element)

        # check if title found
        if title_from_li:
            # format the title and the role
            is_match: bool = is_title_match_role(role, title_from_li)

        else:
            print("Could not find title element")

        return is_match, title_from_li
    except Exception as e:
        print(f"Function: find_and_match_title error: {e}")
        return False, ""


def extract_text_from_href(url: str, description_div_xpath: str) -> str:
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the HTML content with BeautifulSoup using lxml parser
    soup = BeautifulSoup(response.content, 'lxml')

    # Convert the BeautifulSoup object to an lxml Element object
    dom = etree.HTML(str(soup))

    # Define the XPath for the parent element you want to extract

    # Use XPath to find the parent element
    parent_elements = dom.xpath(description_div_xpath)

    if parent_elements:
        parent_element = parent_elements[0]

        # Now, find all <p>, <ul>, and <li> elements within the located parent element
        paragraphs = parent_element.xpath(".//p")
        lists = parent_element.xpath(".//ul")
        list_items = parent_element.xpath(".//li")

        # Extract and concatenate the text content from the child elements
        job_details_text = ""
        for p in paragraphs:
            text = p.xpath('string()')
            if text and len(text.strip()) > 0:
                job_details_text += text.strip() + "\n"

        for ul in lists:
            for li in ul.xpath(".//li"):
                text = li.xpath('string()')
                job_details_text += text.strip() + "\n"

        return job_details_text
    else:
        print("Parent element not found")


def get_href_from_li(element: WebElement) -> str:
    try:
        # extract the "a" tag from the li element
        a_tag = element.find_element(By.TAG_NAME, "a")
        # get the attribute from the "a" tag element
        href = a_tag.get_attribute('href')
        return href
    except Exception as e:
        print(f"Function: get_href_from_li error: {e} ")


def get_job_listings(dto: LinkedinGetJobListingsDto) -> list[str]:
    # region Unpack Dto
    result_list_xpath = dto.result_list_xpath
    wait = dto.wait
    driver = dto.driver
    role = dto.role
    description_div_xpath = dto.description_div_xpath
    show_more_button_xpath = dto.show_more_button_xpath
    # endregion

    # region Get initial result list
    # get the initial job_listings visible on page load
    job_listings: list[WebElement] = get_job_listings_li_elements_list(result_list_xpath, wait)

    if len(job_listings) == 0:
        driver.quit()
        return []
    # endregion

    # region Init variables
    skip_amount = 0
    previous_size = -1
    inserted_descriptions = 0
    job_listings_result_list = []
    urls_attempted_set = set()
    false_title_counter = -1
    increase_every_ten = 0
    repeated_urls_counter = 0
    bad_url_counter = 0
    # endregion

    # region While loop main process
    while job_listings:
        try:
            job_listings_len = len(job_listings)
            # Compare the previous size to know if the list has ended
            if previous_size == job_listings_len:
                break

            # update the size after the check
            previous_size = job_listings_len
            print(f"({dto.role}) Total listings collected: {inserted_descriptions}")

            # Iterate through each job listing, skipping the previously clicked ones
            for i in range(skip_amount, job_listings_len):
                time.sleep(1.5)
                # region Scroll the element into view
                # Start the process bys scrolling to view and clicking the listing
                result: int = scroll_and_click_and_visited_pipeline(driver, job_listings[i],
                                                                    urls_attempted_set)

                # if the job listing was not found or got an error
                if result == 0:
                    bad_url_counter += 1
                    continue

                # if the job listing was already visited
                elif result == 1:
                    repeated_urls_counter += 1
                    continue
                # endregion

                # region Check if the title is matching the role
                is_title_match, title_from_li = find_and_match_title(role, i, job_listings[i], wait)

                if is_title_match is False:
                    false_title_counter += 1
                    continue

                # endregion
                job_url: str = get_href_from_li(job_listings[i])
                xpath='/html/body/main/section[1]/div/div/section[1]/div/div/section/div'
                description: str = extract_text_from_href(job_url, xpath)
                if description:
                    job_listings_result_list.append(description)
                    write_text_to_file('job_description.txt', 'a', description)

                    inserted_descriptions += 1
                else:
                    write_text_to_file('not_found_description.txt', 'a', f"{i} -> {title_from_li}")

            # Update the skip amount for the next iteration
            skip_amount = len(job_listings)

            # Refind the job listings to avoid StaleElementReferenceException
            job_listings = get_job_listings_li_elements_list(result_list_xpath, wait)

        except Exception as e:
            print(e)

    # endregion

    # region Log the result to file and return it
    # log the final result of the function how many listings were collected
    text = f"""
        Inserted descriptions: {inserted_descriptions} 
        Error titles counter: {false_title_counter} 
        Repeated URLS: {repeated_urls_counter}
        Problematic URLS: {bad_url_counter + 1}
        --------------------------------------
        Total Job Listings: {len(job_listings)}
    """
    write_text_to_file('linkdedin_log.txt', 'a', text)

    return job_listings_result_list
    # endregion


def get_job_listings_backup(dto: LinkedinGetJobListingsDto) -> list[str]:
    # region Unpack Dto
    result_list_xpath = dto.result_list_xpath
    wait = dto.wait
    driver = dto.driver
    role = dto.role
    description_div_xpath = dto.description_div_xpath
    show_more_button_xpath = dto.show_more_button_xpath
    # endregion

    # region Get initial result list
    # get the initial job_listings visible on page load
    job_listings: list[WebElement] = get_job_listings_li_elements_list(result_list_xpath, wait)

    if len(job_listings) == 0:
        driver.quit()
        return []
    # endregion

    # region Init variables
    skip_amount = 0
    previous_size = -1
    inserted_descriptions = 0
    job_listings_result_list = []
    urls_attempted_set = set()
    false_title_counter = -1
    increase_every_ten = 0
    repeated_urls_counter = 0
    bad_url_counter = 0
    # endregion

    # region While loop main process
    while job_listings:
        try:
            job_listings_len = len(job_listings)
            # Compare the previous size to know if the list has ended
            if previous_size == job_listings_len:
                break

            # update the size after the check
            previous_size = job_listings_len
            print(f"({dto.role}) Total listings collected: {inserted_descriptions}")

            # Iterate through each job listing, skipping the previously clicked ones
            for i in range(skip_amount, job_listings_len):
                time.sleep(1)
                # region Scroll the element into view
                # Start the process bys scrolling to view and clicking the listing
                result: int = scroll_and_click_and_visited_pipeline(driver, job_listings[i],
                                                                    urls_attempted_set)

                # if the job listing was not found or got an error
                if result == 0:
                    bad_url_counter += 1
                    continue

                # if the job listing was already visited
                elif result == 1:
                    repeated_urls_counter += 1
                    continue
                # endregion

                # region Check if the title is matching the role
                is_title_match, title_from_li = find_and_match_title(role, i, job_listings[i], wait)

                if is_title_match is False:
                    false_title_counter += 1
                    continue

                # endregion
                print(get_href_from_li(job_listings[i]))
                # region Get the full description
                is_successful, description = get_full_description(description_div_xpath,
                                                                  show_more_button_xpath,
                                                                  wait)
                # is_successful, description = True, "test"
                if is_successful:
                    job_listings_result_list.append(description)
                    inserted_descriptions += 1
                else:
                    write_text_to_file('not_found_description.txt', 'a', f"{i} -> {title_from_li}")
                # endregion
            # Update the skip amount for the next iteration
            skip_amount = len(job_listings)

            # Refind the job listings to avoid StaleElementReferenceException
            job_listings = get_job_listings_li_elements_list(result_list_xpath, wait)

        except Exception as e:
            print(e)

    # endregion

    # region Log the result to file and return it
    # log the final result of the function how many listings were collected
    text = f"""
        Inserted descriptions: {inserted_descriptions} 
        Error titles counter: {false_title_counter} 
        Repeated URLS: {repeated_urls_counter}
        Problematic URLS: {bad_url_counter + 1}
        --------------------------------------
        Total Job Listings: {len(job_listings)}
    """
    write_text_to_file('linkdedin_log.txt', 'a', text)

    return job_listings_result_list
    # endregion



def main():

    # bs4 config
    # URL of the webpage to scrape
    bs4_url = 'https://il.linkedin.com/jobs/view/full-stack-engineer-at-bolt-3940304372?position=33&pageNum=0&refId=aVzfZ%2BQM76VnMW572JVktg%3D%3D&trackingId=LVK5lFPxccELa7Ekrths8w%3D%3D&trk=public_jobs_jserp-result_search-card'
    bs4_parent_xpath = '/html/body/main/section[1]/div/div/section[1]/div/div/section/div'


    url = r"https://www.linkedin.com/jobs/search/?currentJobId=3939018469&f_TPR=r604800&geoId=101620260&keywords=backend%20developer&location=Israel&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start=0"
    # full_description_xpath = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div[2]'  # class="description__text description__text--rich"
    full_description_xpath = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div'  # class="description__text description__text--rich"
    show_more_btn_full_xpath = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/button[1]'
    full_description_inner_div_xpath = full_description_xpath + '/section/div'
    result_list_xpath = '/html/body/div[1]/div/main/section[2]/ul'
    drivers = setup_chrome_driver(activate=True, url=url)
    drivers.maximize_window()
    wait = setup_web_driver_wait(drivers)

    dto: LinkedinGetJobListingsDto = LinkedinGetJobListingsDto(
        role='full stack developer',
        driver=drivers,
        wait=wait,
        result_list_xpath= result_list_xpath,
        description_div_xpath=full_description_xpath,
        show_more_button_xpath=show_more_btn_full_xpath
    )
    # res = get_full_description(full_description_inner_div_xpath, show_more_btn_full_xpath, wait)
    # print(res)
    listings = get_job_listings(dto)


if __name__ == '__main__':
    main()
# titles_for_testing = """
# Full Stack Engineer
# Backend Software Engineer - Mid/Senior
# Full Stack Engineer
# Backend Engineer
# Java Software Engineer - LLM
# Backend Engineer
# Full stack developer
# Java developer (Platform engineering)
# Fullstack Developer- Front-End Oriented
# Python Developer
# React.js Developer -LLM Project
# Full Stack Engineer (Backend Oriented)
# Backend Engineer
# Full Stack Engineer
# Senior Full Stack Engineer
# Full Stack Engineer
# Full Stack Engineer
# Backend Developer
# JAVA Developer
# Full Stack Engineer - 4952
# Senior Backend Developer
# Full Stack Developer (Hybrid)
# Senior Back End Developer
# Backend Engineer
# """
