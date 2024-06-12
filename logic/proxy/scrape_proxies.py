import re
from queue import Queue

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame

from logic.proxy.proxy_object import ProxyObjectDto


def get_soup(url: str) -> BeautifulSoup:
    """
    Fetches the HTML content from the given URL and returns a BeautifulSoup object.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    element = 'table'
    element_class = 'table table-striped table-bordered'

    try:
        # Make the GET request to the site
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Error fetching the URL: {e}")

    # Create the bs4 object
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table
    table = soup.find(element, class_=element_class)
    if not table:
        raise ValueError("Table not found in the provided URL with the specified class.")

    return soup


def make_dataframe_from_table(soup: BeautifulSoup, element_class: str) -> pd.DataFrame:
    """
    Parses the HTML table from the BeautifulSoup object and returns it as a DataFrame.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.
        element_class (str): The class attribute of the table element.

    Returns:
        pd.DataFrame: A DataFrame containing the table data.

    Raises:
        ValueError: If the table or its body is not found.
    """
    # Find the table
    table = soup.find('table', class_=element_class)
    if not table:
        raise ValueError("Table not found with the specified class.")

    # Get all the headers
    column_names = table.find_all('th')
    if not column_names:
        raise ValueError("No headers found in the table.")

    # Create DataFrame with column names
    df = pd.DataFrame(columns=[header.text.strip() for header in column_names])

    # Extract rows from the table body
    table_body = table.find('tbody')
    if not table_body:
        raise ValueError("Table body not found.")

    rows = table_body.find_all('tr')

    # Iterate over the rows and extract cell data
    for row in rows:
        columns = row.find_all('td')
        if columns:
            row_data = [col.text.strip() for col in columns]
            df.loc[len(df)] = row_data

    return df


def get_proxies_queue(df: pd.DataFrame) -> Queue[ProxyObjectDto]:
    """
    Extracts proxy addresses from the DataFrame and returns them in a Queue.

    Args:
        df (pd.DataFrame): The DataFrame containing proxy information.
        https (bool): Flag to filter for HTTPS proxies only. Default is True.

    Returns:
        Queue: A queue containing unique proxy addresses in the format IP:Port.
    """
    proxies_queue: Queue[ProxyObjectDto] = Queue()

    for index, row in df.iterrows():
        is_https = row['Https'].lower() == 'yes'
        if not is_https:
            continue
        proxy: ProxyObjectDto = ProxyObjectDto(
            ip_address=row['IP Address'],
            port=row['Port'],
            https=is_https,
        )
        proxies_queue.put(proxy)

    return proxies_queue


def scrape_proxies_pipeline(url: str, element_class: str,) -> Queue[ProxyObjectDto]:
    """
    Scrapes proxy information from the given URL and returns a set of proxies.

    Args:
        url (str): The URL of the proxy list website.
        element_class (str): The class attribute of the table element.
        https (bool): Flag to filter for HTTPS proxies only. Default is True.

    Returns:
        Queue[str]: A queue of proxy addresses in the format IP:Port.
    """
    try:
        # Get the soup
        soup = get_soup(url)

        # Extract the table and make it DataFrame
        df = make_dataframe_from_table(soup, element_class)

        # Create the proxies set from the DataFrame
        proxies_queue = get_proxies_queue(df)

        return proxies_queue
    except Exception as e:
        print(f"An error occurred: {e}")
        return set()
