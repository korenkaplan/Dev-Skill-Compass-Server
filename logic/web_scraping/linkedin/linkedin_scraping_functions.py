"""This module contains the scraping logic for LinkedIn site"""

import json
import re
import time
from random import uniform
import requests
from bs4 import BeautifulSoup
from logic.web_scraping.linkedin.title_filtering import is_title_match_role
from utils.functions import retry_function, write_text_to_file
from requests.exceptions import RequestException, SSLError


# region Sub Functions
def filter_li_elements_by_title_action(li_elements: list, role: str, log_file_path: str) -> (list, list):
    title_filtered_li_elements = []
    titles = []
    for li in li_elements:
        try:
            tag = li.find('h3')
            if tag is None:
                raise ValueError(f"No 'h3' tag found in 'li' element: {li}")

            title = tag.text.strip()
            if is_title_match_role(role, title, log_file_path):
                title_filtered_li_elements.append(li)
                titles.append(title)
        except Exception as e:
            raise RuntimeError(f"Error processing 'li' element: {e}")

    return titles, title_filtered_li_elements


def filter_li_elements_by_title(soup: BeautifulSoup, role: str, log_file_path: str, visited_postings: set) -> (list, int):
    try:
        li_elements = soup.find_all('li')
        skip_amount = len(li_elements)
        if not li_elements:
            raise ValueError("No 'li' elements found in the provided HTML.")
    except Exception as e:
        raise RuntimeError(f"Error finding 'li' elements: {e}")

    titles, title_filtered_li_elements = filter_li_elements_by_title_action(li_elements, role, log_file_path)

    title_filtered_li_elements = filter_by_unique_title_and_location(titles, title_filtered_li_elements, visited_postings)


    return title_filtered_li_elements, skip_amount


def filter_by_unique_title_and_location(titles: list, li_elements: list,  visited_postings: set):
    filtered_li_elements = []
    for li, title in zip(li_elements, titles):
        company, location = get_company_and_location(li)
        title = title.strip().replace('senior', '').replace('junior', '')
        unique_title = company + location + title
        unique_title = unique_title.lower(). replace(' ', '').replace(',', '')


        if unique_title not in visited_postings:
            filtered_li_elements.append(li)
            visited_postings.add(unique_title)
        else:
            write_text_to_file('repeated_descriptions.txt', 'a', unique_title)

    return filtered_li_elements


def get_company_and_location(li_element: BeautifulSoup) -> (str, str):
    company = li_element.find('h4')
    location = li_element.find('span', class_='job-search-card__location')
    return company.text.strip(), location.text.strip()


def get_job_details_text(url, tag_name: str, class_name: str):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the div element with the specific class names
    job_details_div = soup.find(tag_name, class_=class_name)
    if not job_details_div:
        return "No job details found"

    # Replace <br> tags with newline characters
    for br in job_details_div.find_all('br'):
        br.replace_with('\n')

    # Extract the text
    text = job_details_div.get_text(separator=' ', strip=True)

    # Split the text by newlines to get rows
    lines = text.split('\n')

    # Combine the lines into a single string with newlines
    result = '\n'.join(line.strip() for line in lines)

    return result


def get_li_hrefs(visited_postings_set: set, url: str, role: str, log_file_path, proxy=None) -> (list, int):
    i = 0
    try:
        # Setup proxy if provided
        proxies = {
            "http": proxy,
            "https": proxy,
        } if proxy else None

        # Send a request to the URL
        response = requests.get(url, proxies=proxies)

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"(get_li_hrefs) -> Failed to retrieve the webpage. Status code: {response.status_code}")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        li_elements_filtered, skip_amount = filter_li_elements_by_title(soup, role, log_file_path, visited_postings_set)
        # Extract the href attributes from the 'a' tags inside the 'li' elements
        hrefs = []
        for li in li_elements_filtered:
            a_tag = li.find('a', href=True)
            if a_tag:
                hrefs.append(a_tag['href'])

        return hrefs, skip_amount

    except RequestException as e:
        raise Exception(f"(get_li_hrefs) -> Request failed: {e}")

    except Exception as e:
        raise Exception(f"(get_li_hrefs) -> An error occurred: {e}")


def get_text_from_href(href: str) -> str:
    try:
        # Send a GET request to the URL with the proxy
        response = requests.get(href, timeout=5)
        response.raise_for_status()  # Check that the request was successful

        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the script tag containing JSON-LD
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            # Load the JSON content
            job_data = json.loads(script_tag.string)

            # Extract the description and decode HTML entities
            description = job_data.get('description', '')
            description_soup = BeautifulSoup(description, 'html.parser')

            description_text = description_soup.get_text()

            new_text = re.sub(r'(<br\s*/?>|</?li>|</?p>)', ' ', description_text)
            new_text = re.sub(r'(<strong>|</strong>|<ul>|</ul>|<span>|</span>|<em>|</em>|<u>|</u>)', '', new_text)
            return new_text
        else:
            raise Exception("(get_text_from_href) -> JSON-LD script tag not found")
    except SSLError as e:
        raise Exception(f"(get_text_from_href) -> SSL error: {e}")
    except RequestException as e:
        raise Exception(f"(get_text_from_href) -> Request failed: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"(get_text_from_href) -> JSON decoding failed: {e}")
    except Exception as e:
        raise Exception(f"(get_text_from_href) -> An error occurred: {e}")


def get_job_listings(url: str, role: str, log_file_path: str, proxy=None) -> list:
    """
    Fetch job listings descriptions from the specified URL with optional proxy support.

    Parameters:
    - url: The base URL to fetch job listings from.
    - proxy: Optional proxy to use for the requests.

    Returns:
    - A list of job listings descriptions.
    """
    # Variables
    skip_amount = 340
    job_listings_descriptions = []
    max_attempts = 3
    visited_postings_set = set()
    visited_hrefs_counter = 0
    failed_attempts_counter = 0
    title_filtered_listings_counter = 0
    # Each iteration of the loop is a fetch request and loop over the listings from that request.
    while True:
        print(f"Total Inserted: {len(job_listings_descriptions)}")
        # Set the initial variables for each iteration: unique sleep time each iteration, pagination on the skip amount
        sleep_time = uniform(4.0, 5.0)
        formatted_url = url + str(skip_amount)

        try:
            # Fetch the href attribute of the job listings from the site.
            hrefs, scanned_listings_amount = retry_function(get_li_hrefs, role_name=role, max_attempts=3,
                                                            delay=sleep_time,
                                                            backoff=1, visited_postings_set=visited_postings_set,
                                                            url=formatted_url, role=role,
                                                            log_file_path=log_file_path, proxy=proxy)

            # count the number of listings with title not matching the role.
            # total amount per get request (10) - the amount of filtered fetched listings = the amount of error listings
            title_filtered_listings_counter += scanned_listings_amount - len(hrefs)
        except Exception as e:
            print(f"Failed to fetch job listings: {e}")
            break

        # **Stopping condition** if hrefs is empty: Means that the list is over and there are no more listings, break.
        if not hrefs:
            break

        # Update the skip amount for the next fetch
        skip_amount += scanned_listings_amount

        # Iterate through the list of hrefs fetched from the server
        for href in hrefs:
            try:
                # Try to fetch the description from the href attribute of the job listings
                description: str = retry_function(get_text_from_href, role_name=role, max_attempts=max_attempts,
                                                  delay=sleep_time, backoff=2, href=href)
                if description:
                    # If there is a description, add to the list
                    write_text_to_file('new_descriptions.txt', 'a', description)
                    job_listings_descriptions.append(description)

            except Exception as e:
                failed_attempts_counter += 1
                print(f"Failed to fetch job description: {e}")

        # Sleep time after fetching all the descriptions fetched in the request
        time.sleep(sleep_time)

    # After fetching all the listings, return the descriptions list
    text: str = f"""
    Inserted descriptions: {len(job_listings_descriptions)} 
    Repeated URLS: {visited_hrefs_counter}
    Failed to fetch description: {failed_attempts_counter}
    Title not matching role: {title_filtered_listings_counter}
    --------------------------------------
    Total Job Listings: {skip_amount}
    """
    write_text_to_file(log_file_path, 'a', text)
    return job_listings_descriptions


# endregion

def get_listings_from_linkedin(base_url: str, role: str, log_file_path: str) -> list:
    """
    Wrapper function to fetch job listings from LinkedIn.

    Parameters:
    - base_url: The base URL to fetch job listings from.
    - role: The job role to filter listings by.

    Returns:
    - A list of job listings descriptions.
    """
    sleep_time = uniform(10.0, 30.0)
    return retry_function(get_job_listings, role_name=role, max_attempts=5, delay=sleep_time, backoff=1,
                          url=base_url, role=role, log_file_path=log_file_path)


def main():
    log_file_path = r"C:\Users\Koren Kaplan\Desktop\Dev-Skill-Compass-Server\logic\web_scraping\Logs\linkedin"
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=frontend%2bdeveloper&location=Israel&geoId=101620260&f_TPR=r604800&start=0"
    listings = get_listings_from_linkedin(url, 'frontend developer', log_file_path)

    for i, job in enumerate(listings):
        print(f"{i} -> {job}")
        print(500 * "=")


if __name__ == '__main__':
    main()
