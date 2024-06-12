import json
import re
from fp.fp import FreeProxy
from time import sleep

import requests
from bs4 import BeautifulSoup
from lxml import etree

from logic.web_scraping.linkedin.linkedin_scraping import fetch_url_with_retries
from utils.functions import write_text_to_file


def get_li_hrefs(url):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all 'li' elements
    li_elements = soup.find_all('li')

    # Extract the href attributes from the 'a' tags inside the 'li' elements
    hrefs = []
    for li in li_elements:
        a_tag = li.find('a', href=True)
        if a_tag:
            hrefs.append(a_tag['href'])

    return hrefs


def extract_text_from_href(url: str, description_div_xpath: str) -> str:
    # Send a GET request to fetch the raw HTML content
    response = fetch_url_with_retries(url, 3)
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


def find_row(href: str, phrase: str):
    # define variables
    response = requests.get(href)
    response.raise_for_status()  # Check that the request was successful

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.content, 'html.parser')
    text = str(soup)
    # Split the multi-line string into lines
    lines = text.split('\n')
    script_tag = soup.find('script', type='application/ld+json')
    if script_tag:
        # Load the JSON content
        job_data = json.loads(script_tag.string)

        # Extract the description and decode HTML entities
        description = job_data.get('description', '')
        description = BeautifulSoup(description, 'html.parser').get_text()

        print(description)
    else:
        print("JSON-LD script tag not found")
    # Iterate through the lines and check for the substring
    for i, line in enumerate(lines):
        if phrase in line:
            print(f"Substring '{phrase}' found in line {i + 1}: {line}")
            break
    else:
        print(f"Substring '{phrase}' not found in any line.")


def get_text_from_href(href: str):
    try:
        # Send a GET request to the URL
        response = requests.get(href)
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

            new_text = re.sub(r'(<br\s*/?>|</?li>|</?p>)', '\n', description_text)
            new_text = re.sub(r'(<strong>|</strong>|<ul>|</ul>)', '', new_text)
            return new_text
        else:
            return "JSON-LD script tag not found"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    except json.JSONDecodeError as e:
        return f"JSON decoding failed: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def main_pipeline():
    first_job_index = 0
    class_name = 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden'
    tag_name = 'div'
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Backend%2BDeveloper&location=Israel&geoId=101620260&f_TPR=r604800&start="
    job_listings = []
    counter = 0
    while True:
        formatted_url = url + str(first_job_index)
        print(formatted_url)
        # get the hrefs from the li elements
        hrefs: list = get_li_hrefs(formatted_url)

        # Stopping condition
        if len(hrefs) == 0:
            break
        # update first job index to the length of the list so that we know where to start from next
        first_job_index += len(hrefs)
        for href in hrefs:
            # get the text from the href url
            # description: str = get_job_details_text(href, tag_name, class_name)
            description: str = get_text_from_href(href)
            # add the text to job listings
            if description:
                counter += 1
                print(f"{counter} -> inserted")
                job_listings.append(description)
                # write the listings to file
    return job_listings





def main():
        proxies = FreeProxy(https=True, rand=True).get_proxy_list(0)
        print(proxies)
        dics = {}
        for proxy in proxies:
            dics

        proxies_dict = {'https': f'https://{proxy}' for proxy in proxies}
        print(proxies_dict)
    # listings = main_pipeline()
    # print(len(listings))


if __name__ == '__main__':
    main()


